# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to implement an AWS Lambda function that handles input from direct
invocation.
"""

import easyocr
import json
import base64
from io import BytesIO
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], detector=False, gpu=False, download_enabled=False, model_storage_directory='model_file', user_network_directory='user_network')

def handler(event, context):
    """
    Accepts an action and a number, performs the specified action on the number,
    and returns the result.

    :param event: The event dict that contains the parameters sent when the function
                  is invoked.
    :param context: The context in which the function is called.
    :return: The result of the specified action.
    """
    # NOTE: get image
    try:
        event_body = json.loads(event['body'].encode('utf-8'))
        image = event_body['image'] # string type
    except KeyError as e:
        print(f"KeyError: {e}")
        image = event['image']
    if image == 'trigger':
        return {
            'statusCode': 200,
            'body': json.dumps(
                {
                    "message": 'trigger successful',
                }
            )
        }
    else:
        # decoded_byte = base64.b64decode(image)
        # pil_img = Image.open(BytesIO(base64.b64decode(image))).convert('L')
        # np_img = np.array(Image.open(BytesIO(base64.b64decode(image))).convert('L'))
        result = reader.recognize(np.array(Image.open(BytesIO(base64.b64decode(image))).convert('L')))
        response = {'result': result}
    return response

