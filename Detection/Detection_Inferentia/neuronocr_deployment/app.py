"""
Flask app to detect text from images deployed on AWS inferentia
"""

import json
import gc
import base64
import cv2
import time
import torch
import torch_neuron
import numpy as np
from PIL import Image
from io import BytesIO
from waitress import serve
from flask import Flask, request
from logging import getLogger
app = Flask(__name__)
from neuronocr_compilation import easyocr


LOGGER = getLogger(__name__)
ocr_reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False,
                            download_enabled=True, model_storage_directory='model_file',
                            user_network_directory='user_network')
neuron_model = torch.jit.load('/home/inference/api/neuronocr_deployment/model_file/ocr_neuron.pt')


@app.route("/", methods=["GET"])
def home():
    print("Hello World!")
    return "Hello World!"


def predict_bbox(image, model, ocr_reader):
    '''
    This function resizes the input image and generate prediction for detected text.
    :param image: Base64 decoded image
    :param model: Inferentia compatible neuron model
    :param ocr_reader: OCR object
    :return: Coordinates for detected text
    '''
    # model was compiled using images size (224, 224)
    resized_image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    result = ocr_reader.detect(resized_image, net=model)
    # Flask response data should be converted to int
    int_result = ([[[int(i) for i in small_list] for small_list in result[0][0]]],
                  [[[int(j) for j in smal_list] for smal_list in result[1][0]]])
    response = {'result': int_result}
    return response


@app.route('/predict', methods=["POST"])
def detect_text():
    '''
    Load the image data from flask request.
    Pass the decoded image to predict_bbox function to generate predictions.
    :return: (Flask response data) Coordinates for detected text
    '''
    # load the image from request data
    try:
        # with API gateway
        event_body = json.loads(request.data)['body']
        event_body = json.loads(event_body)
        image = event_body['image']
    except KeyError as e:
        # without API gateway
        image = json.loads(request.data)['image']

    # decode the base64 encoded input image
    image = np.array(Image.open(BytesIO(base64.b64decode(image))).convert('L'))
  
    # inference
    response_data = predict_bbox(image, neuron_model, ocr_reader)
    
    # clean up and return
    del image
    gc.collect()
    return response_data


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
    '''
    Ports are configured as follows:
    5000:8080 -> docker_port:flask_port
    http://localhost:8080 #docker
    http://localhost:5000 #flask
    '''