from neuronocr_compilation import easyocr
# get_detector function to load model separately
from neuronocr_compilation.easyocr.detection import get_detector

img_dir = r'/home/ubuntu/ssl/Detection_Inferentia/neuronocr_deployment/images'

def main():
    '''
    Function to test the function of OCR detection part.
    This function loads the model separately, detects text and returns the result
    :return: Tuple of coordinates for detected texts
    '''
    ocr_reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False,
                                download_enabled=True, model_storage_directory='model_file',
                                user_network_directory='user_network')
    model = get_detector(r'model_file/craft_mlt_25k.pth')
    image_path = img_dir + '/facebook.jpg'
    result = ocr_reader.detect(image_path, net=model)
    return result


if __name__ == '__main__':
    bbox = main()
    print(bbox)
