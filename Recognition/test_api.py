import requests
import base64
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json
import time
import os
import sys

file_name = 'some_path/your_image.jpg'
with open(file_name, 'rb') as f:
    image_bytes = f.read()

lambda_url = "http://localhost:8080/2015-03-31/functions/function/invocations"

# simulate without API gateway
payload = {"image": "trigger"}
# simulate API gateway
payload = {"body": '{"image": "trigger"}'}

# actual image test, simulate without API gateway
payload = {"image": base64.b64encode(image_bytes).decode()}
# actual image test, simulate API gateway
payload = {"body": '{"image": "' + base64.b64encode(image_bytes).decode() + '", ' + \
                   '"language": "en"}'}


headers = {'Content-type': 'application/json'}
start_time = time.time()
response = requests.post(
    lambda_url,
    data=json.dumps(payload),
    headers=headers
)
print(response)
print(response.content)
print(response.json())