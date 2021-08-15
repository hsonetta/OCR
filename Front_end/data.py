import os

# Style Models Data

lang_models_file = ['english_g2.pth']

lang_models_name = ['English']

model_path = 'models'

style_models_dict = {name: os.path.join(model_path, filee) for name, filee in zip(lang_models_name, lang_models_file)}

# Style Images Data

content_images_file = ['ocrimage.jpg', 'quote1.jpg', 'numberplate.jpg', 'english.jpg']

content_images_name = ['OCR Image', 'AI Quote', 'Number Plate', 'English']

images_path = 'images'

content_images_dict = {name: os.path.join(images_path, filee) for name, filee in zip(content_images_name, content_images_file)}
