import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

lambda_url = os.environ.get("lambda_url")

def detect_text(image):
    #kubernetes endpoint
    #post request and get the output
    pass

def recognize_text(image):

    headers = {'Content-type': 'application/json'}
    response = requests.post(
        lambda_url,
        data=json.dumps(image),
        headers=headers
    )
    response = response.json()
    return response