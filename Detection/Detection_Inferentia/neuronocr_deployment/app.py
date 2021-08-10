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
from neuronocr_compilation.easyocr.detection import get_detector


LOGGER = getLogger(__name__)
ocr_reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False,
                            download_enabled=True, model_storage_directory='model_file',
                            user_network_directory='user_network')
neuron_model = torch.jit.load('/home/inference/api/neuronocr_deployment/model_file/ocr_neuron.pt')
normal_model = get_detector(r'/home/inference/api/neuronocr_deployment/model_file/craft_mlt_25k.pth')
# normal_model = get_detector(r'model_file/craft_mlt_25k.pth')


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
    # Flask response data should be converted from int32 to int
    coordinates = ([list(map(int, _)) for _ in result[0][0]])
    return coordinates


@app.route('/predict', methods=["POST"])
def detect_text():
    '''
    Load the image data from flask request.
    Pass the decoded image to predict_bbox function to generate predictions.
    :return: (Flask response data) Coordinates for detected text
    '''
    # load the image from request data
    try:
        image = json.loads(request.data)['image']
    except KeyError:
        return {'body': json.dumps('Enter the image in the request')}

    # decode the base64 encoded input image
    image = np.array(Image.open(BytesIO(base64.b64decode(image))).convert('L'))
  
    # inference
    start = time.time()
    try:
        model_type = json.loads(request.data)['model_type']
    except KeyError:
        return {'body': json.dumps('Enter model_type argument in request')}

    if model_type == 0: #normal model
        response_data = predict_bbox(image, normal_model, ocr_reader)
    else: #neuron model
        response_data = predict_bbox(image, neuron_model, ocr_reader)

    end = time.time()
    inf_time = end-start
    
    # clean up and return
    del image
    gc.collect()
    return {
            'statusCode': 200,
            'body': json.dumps(
                {
                    'message': 'ocr detection success',
                    'coordinates': response_data,
                    'inference_time_sec': inf_time
                }
            )
    }

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
    '''
    Ports are configured as follows:
    5000:8080 -> docker_port:flask_port
    http://localhost:8080 #docker
    http://localhost:5000 #flask
    '''