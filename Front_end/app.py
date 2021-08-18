"""
App file to layout front-end and call the image input function
"""
import streamlit as st
from data import *
from input import image_input

st.title("Text Recognition")
st.sidebar.title('Navigation')
method = st.sidebar.radio('Go To ->', options=['Image'])
st.sidebar.header('Options')

style_model_name = st.sidebar.selectbox("Choose the language model: ", lang_models_name)

if method == 'Image':
    image_input(style_model_name)