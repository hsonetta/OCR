from neuronocr_compilation import easyocr

#import the get_detector function to load the net separately
from neuronocr_compilation.easyocr.detection import get_detector

reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False, download_enabled=True, model_storage_directory='model_file', user_network_directory='user_network')
network = get_detector(r'model_file\craft_mlt_25k.pth')
image = 'images/facebook.jpg'
result = reader.detect(image, net=network)
print(result)
