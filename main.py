import streamlit as st
from PIL import Image
from encoder import encode_message
from decoder import decode_message

st.title("Image Steganography Tool")

option = st.radio("Select Mode", ["Encode", "Decode"])

if option == "Encode":
    uploaded_file = st.file_uploader("Upload Image to Encode", type=["png", "jpg", "jpeg"])
    message = st.text_area("Enter Message to Hide")
    password = st.text_input("Enter Passcode:", type="password")
    if uploaded_file and message and password:
        image = Image.open(uploaded_file)
        encode_message(image, message, password)

elif option == "Decode":
    uploaded_file = st.file_uploader("Upload Encrypted Image", type=["png", "jpg", "jpeg"])
    password = st.text_input("Enter Passcode:", type="password")
    if uploaded_file and password:
        image = Image.open(uploaded_file)
        decode_message(image, password)