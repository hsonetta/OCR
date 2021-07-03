#!/usr/local/bin/python3
"""
adapted from test.py to use flask to serve
"""

# -*- coding: utf-8 -*-
import flask
from flask import Flask, request
app = Flask(__name__)

from waitress import serve
import json
import gc
from PIL import Image
from io import BytesIO
import numpy as np
import torch
import torch_neuron
import easyocr
import base64
import cv2

@app.route("/predict", methods=["GET"])
def home():
    print("Hello World!")
    return "Hello World!"

def predict(image, net, ocr_reader):
    resized_image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    result = ocr_reader.detect(resized_image, net=net)
    int_result = ([[[int(i) for i in small_list] for small_list in result[0][0]]], [[[int(j) for j in smal_list] for smal_list in result[1][0]]])
    response = {'result':int_result}
    return response

@app.route('/predict', methods=["POST"])
def detect_text():
    image = json.loads(request.data)['image']
    image = np.array(Image.open(BytesIO(base64.b64decode(image))).convert('L'))

    ocr_reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False, download_enabled=False,
                                model_storage_directory='model_file', user_network_directory='user_network')
    net = torch.jit.load('ocr_neuron.pt')
  
    # inference
    response_data = predict(image, net, ocr_reader)
    
    # clean up and return
    del image
    gc.collect()
    return response_data

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
    '''
    Ports are configured as follows:
    nvidia-docker run -p 5000:8080 wernerchao/craftapi:craftapi-v0-0-0-1
    5000:8080 -> docker_port:flask_port
    http://localhost:5000
    '''