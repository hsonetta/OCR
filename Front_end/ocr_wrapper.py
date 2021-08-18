import os
import json
import requests
import base64
import cv2
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

lambda_url = os.environ.get("lambda_url")

@st.cache(suppress_st_warning=True)
def detect_text(image, ocr_reader):
    # actual image
    result = ocr_reader.detect(image)
    return result[0]

def crop_img(image, coords):
    crop_images = []
    for coord in coords:
        crop_img = image[coord[2]:coord[3], coord[0]:coord[1]]
        crop_images.append(crop_img)
    return crop_images

@st.cache(suppress_st_warning=True)
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