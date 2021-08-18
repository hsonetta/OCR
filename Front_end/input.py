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
import time

@st.cache(suppress_st_warning=True)
def load_ocr():
    ocr_reader = easyocr.Reader(['en'], detector=True, recognizer=False, gpu=False,
                            download_enabled=False, model_storage_directory='model_file',
                            user_network_directory='user_network')
    return ocr_reader


def image_input(lang_models_name):
    content_name = st.sidebar.selectbox("Choose the images:", content_images_name)
    content_file = content_images_dict[content_name]
    if st.sidebar.checkbox('Upload'):
        content_file = st.sidebar.file_uploader("Choose an Image", type=["png", "jpg", "jpeg"])

    if content_file is not None:
        #Image for display
        image = Image.open(content_file)
        image = np.array(image) #pil to cv
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    else:
        st.warning("Upload an Image OR Untick the Upload Button)")
        st.stop()

    ocr_reader = load_ocr()
    start = time.time()
    #detect text
    text_coordinates = detect_text(image, ocr_reader) #pass base64 image (base64 str)
    #crop small images
    crop_images = crop_img(image, text_coordinates) #pass cv2 image for cropping (cv2 image, [[[x0,y0],[x1,y1],[x2,y2],[x3,y3]]])
    #recognize text
    text, conf_score, inf_time = recognize_text(crop_images) #cropped numpy images (list)
    end = time.time()

    inf_time = round(end - start, 3)
    st.markdown('**Image:**')
    st.image(image, width=400, channels='BGR')
    st.write('**Recognized Text**: ', text)
    st.write('**Confidence Score:** ', conf_score)
    st.write('**Inference Time (sec):** ', inf_time)

