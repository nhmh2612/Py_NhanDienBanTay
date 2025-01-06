import streamlit as st
import cv2
import numpy as np
from PIL import Image
from styles import apply_styles
from about import show_about_app
from SLtoText import SLtoText
from interface import speech_to_sign_ui


apply_styles()

st.sidebar.markdown('<p class="sidebar-title">Image Processing & Computer Vision</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-subheader">Sign Language Detection</p>', unsafe_allow_html=True)

@st.cache_data()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

# Dropdown for app mode
app_mode = st.sidebar.selectbox('Choose the App mode', [
    'About App', 
    'Sign Language to Text', 
    'Text to Sign Language'
])

# Create an empty container to clear content between different modes
placeholder = st.empty()

# Container to ensure that each mode has its own space
with st.container():
    if app_mode == 'About App':
        # Clear the current container and show About App
        
        show_about_app()  # Display About App content

    elif app_mode == 'Sign Language to Text':
        # Clear the current container and show Sign Language to Text
        SLtoText()  # Display Sign Language to Text content

    elif app_mode == 'Text to Sign Language':
        # Clear the current container and show Text to Sign Language
        speech_to_sign_ui()  # Display Text to Sign Language content
