import easyocr

reader = easyocr.Reader(['en'], detector=False, gpu=False)
result = reader.recognize('blackonwhite.jpg')
print(result)