#!/usr/local/bin/python3
"""
adapted from test.py to use flask to serve
"""

# -*- coding: utf-8 -*-
import flask
from flask import Flask
app = Flask(__name__)

from waitress import serve
import time
import gc
from PIL import Image
from io import BytesIO
import numpy as np


def predict(image, net):
    pass



@app.route('/predict', methods=["POST"])
def main():
    t = time.time()
    response_data = {"success": False}

    # load data
    if flask.request.files.get("image"):
        image = flask.request.files["image"].read()
        image = np.array(Image.open(BytesIO(image)).convert('RGB'))
  
    # inference
    response_data = predict(image, net) # TODO: pass in your net here
    
    # clean up and return
    del image
    gc.collect()
    return flask.jsonify(response_data)


@app.route("/", methods=["GET"])
def home():
    print("Hello World!")
    return "Hello World!"


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    serve(app, host='0.0.0.0', port=5000) # waitress
    '''
    Ports are configured as follows:
    nvidia-docker run -p 5000:8080 wernerchao/craftapi:craftapi-v0-0-0-1
    5000:8080 -> docker_port:flask_port
    http://localhost:5000
    '''