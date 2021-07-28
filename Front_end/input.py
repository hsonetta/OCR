"""
Loads the desired input image, language model
and calls function to recognize text.
"""
import numpy as np
import streamlit as st
from PIL import Image
import cv2
from neural_style_transfer import recognize_text
from data import *
import base64


def image_input(lang_models_name):
    if st.sidebar.checkbox('Upload'):
        content_file = st.sidebar.file_uploader("Choose an Image", type=["png", "jpg", "jpeg"])
    else:
        content_name = st.sidebar.selectbox("Choose the images:", content_images_name)
        content_file = content_images_dict[content_name]

    if content_file is not None:
        #Image for display
        content = Image.open(content_file)
        content = np.array(content) #pil to cv
        content = cv2.cvtColor(content, cv2.COLOR_RGB2BGR)
        #base64 image for recognition
        with open(content_file, 'rb') as f:
            image_bytes = f.read()
        str_image = {"image": base64.b64encode(image_bytes).decode()}
    else:
        st.warning("Upload an Image OR Untick the Upload Button)")
        st.stop()

    generated = recognize_text(str_image)
    st.sidebar.image(content, width=300, channels='BGR')
    st.write('Text : ', str(generated['payload']['text']))
    st.write('Confidence Score: ', round(generated['payload']['conf'], 3))
    st.write('Inference Time (ms): ', round(generated['inference_time_ms'], 3))