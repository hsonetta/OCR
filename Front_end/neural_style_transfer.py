import os
import json
import requests
import base64
import cv2
from dotenv import load_dotenv
load_dotenv()

lambda_url = os.environ.get("lambda_url")
inferentia_url = os.environ.get("inferentia_url")


def detect_text(image_str):
    # actual image
    headers = {'Content-type': 'application/json'}
    response = requests.post(
        inferentia_url,
        data=image_str)
    response = response.json()
    text_coordinates = response['predicted']['textlines']
    return text_coordinates


def recognize_text(crop_images):
    text, conf_score, inf_time = [], [], []
    for img in crop_images:
        success, image_byte = cv2.imencode('.png', img)
        image_byte = image_byte.tobytes()
        payload = {"image": base64.b64encode(image_byte).decode()}

        headers = {'Content-type': 'application/json'}
        response = requests.post(
            lambda_url,
            data=json.dumps(payload),
            headers=headers
        )
        response = response.json()
        text.append(str(response['payload']['text']))
        conf_score.append(response['payload']['conf'])
        inf_time.append(response['inference_time_ms'])
    return ' '.join(text), round(sum(conf_score)/len(conf_score), 3), round(sum(inf_time)/len(inf_time), 3)