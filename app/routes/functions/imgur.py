from os import environ
from urllib.request import urlopen
import requests
CLIENT_ID = environ.get("IMGUR_CLIENT_ID")
CLIENT_SECRET = environ.get("IMGUR_CLIENT_SECRET")
from imgurpython import ImgurClient
from flask import send_file, make_response
import io
from werkzeug.utils import secure_filename
import os
import tempfile
from urllib.parse import urlparse, parse_qs

imgur_client = ImgurClient(CLIENT_ID, CLIENT_SECRET)

def image_upload(url):
    uploaded_image = imgur_client.upload_from_url(url, anon=True)
    return uploaded_image['link']


def get_image_hash(image_url):
    try:
        url_segments = image_url.split('/')
        
        for segment in url_segments:
            if '.j' in segment:
                image_hash = segment.split('.')[0]
                print(image_hash)
                return image_hash
            
        print("Image hash not found in URL.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def export_image(img_url):
    image_hash = get_image_hash(img_url)
    headers = {
    'Authorization': f'Client-ID {CLIENT_ID}'
    }
    response = requests.get('https://api.imgur.com/3/credits', headers=headers)
    response = requests.get(f'https://api.imgur.com/3/image/{image_hash}', headers=headers)
                
    if response.status_code == 200:
        image_data = response.json()
        image_url = image_data['data']['link']
        print(f"Image URL: {image_url}")
        
        import certifi
        import urllib3

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', image_url)
        
        with open('image.jpeg', "wb") as fd_out:
            fd_out.write(response.data)
    
def upload_image_from_file(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(tempfile.gettempdir(), filename)
    file.save(filepath)
    
    uploaded_image = imgur_client.upload_from_path(filepath, anon=True)
    
    os.remove(filepath)
    
    return uploaded_image['link']
