from os import environ
import requests
CLIENT_ID = environ.get("IMGUR_CLIENT_ID")
CLIENT_SECRET = environ.get("IMGUR_CLIENT_SECRET")
from imgurpython import ImgurClient

imgur_client = ImgurClient(CLIENT_ID, CLIENT_SECRET)

def image_upload(url):
    uploaded_image = imgur_client.upload_from_url(url, anon=True)
    return uploaded_image['link']