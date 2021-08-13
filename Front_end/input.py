"""
Loads the desired input image, language model
and calls function to recognize text.
"""
import numpy as np
import streamlit as st
from PIL import Image
import cv2
from ocr_wrapper import detect_text, crop_img, recognize_text
from data import *
import easyocr

ocr_reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False,
                            download_enabled=False, model_storage_directory='model_file',
                            user_network_directory='user_network')

def image_input(lang_models_name):
    if st.sidebar.checkbox('Upload'):
        content_file = st.sidebar.file_uploader("Choose an Image", type=["png", "jpg", "jpeg"])
    else:
        content_name = st.sidebar.selectbox("Choose the images:", content_images_name)
        content_file = content_images_dict[content_name]

    if content_file is not None:
        #Image for display
        image = Image.open(content_file)
        image = np.array(image) #pil to cv
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    else:
        st.warning("Upload an Image OR Untick the Upload Button)")
        st.stop()

    #detect text
    text_coordinates = detect_text(image, ocr_reader) #pass base64 image (base64 str)
    #crop small images
    crop_images = crop_img(image, text_coordinates) #pass cv2 image for cropping (cv2 image, [[[x0,y0],[x1,y1],[x2,y2],[x3,y3]]])
    #recognize text
    text, conf_score, inf_time = recognize_text(crop_images) #cropped numpy images (list)

    st.sidebar.image(image, width=300, channels='BGR')
    st.write('Text : ', text)
    st.write('Confidence Score: ', conf_score)
    st.write('Inference Time (sec): ', inf_time)

