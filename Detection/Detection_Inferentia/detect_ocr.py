import easyocr
import base64
from io import BytesIO
import numpy as np
from PIL import Image

from easyocr.detection import get_detector

reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False, download_enabled=False, model_storage_directory='model_file', user_network_directory='user_network')
network = get_detector(r'C:\Users\hsone\Desktop\SharpestMinds\EasyOCR\Detection\EasyOCR\model_file\craft_mlt_25k.pth')
image = 'images/facebook.jpg'
result = reader.detect(image, net=network)
print(result)
