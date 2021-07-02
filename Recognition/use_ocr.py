import easyocr

reader = easyocr.Reader(['en'], detector=False, gpu=False, download_enabled=False, model_storage_directory='model_file', user_network_directory='user_network')
result = reader.recognize('blackonwhite.jpg')
print(result)