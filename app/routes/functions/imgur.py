from os import environ
import requests
CLIENT_ID = environ.get("IMGUR_CLIENT_ID")
CLIENT_SECRET = environ.get("IMGUR_CLIENT_SECRET")
from imgurpython import ImgurClient
from flask import send_file
from werkzeug.utils import secure_filename
import os
import tempfile

imgur_client = ImgurClient(CLIENT_ID, CLIENT_SECRET)

def image_upload(url):
    uploaded_image = imgur_client.upload_from_url(url, anon=True)
    return uploaded_image['link']

def export_image(img_id):
    image = imgur_client.get_image(img_id)
    if image:
        # Get the direct link to the image
        image_link = image.link
        
        # Set up the file name for the downloaded image
        filename = f"image_{img_id}.jpg"  # You can change the file extension based on the actual image format
        
        # Download the image to a file
        img_response = requests.get(image_link)
        with open(filename, 'wb') as f:
            f.write(img_response.content)
        
        # Send the file as a direct download to the user's device
        return send_file(filename, as_attachment=True)
    else:
        # If the image details cannot be retrieved, return an error message
        return "Error: Unable to fetch the image details from Imgur"
    
def upload_image_from_file(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(tempfile.gettempdir(), filename)
    file.save(filepath)
    
    # Now filepath contains the path to the saved file
    uploaded_image = imgur_client.upload_from_path(filepath, anon=True)
    
    # Don't forget to remove the temporary file after uploading
    os.remove(filepath)
    
    return uploaded_image['link']
