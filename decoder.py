import cv2
import streamlit as st
from PIL import Image
import numpy as np

def decode_message(image, entered_password=None):
    try:
        img = np.array(image.convert("RGB"))
        h, w, _ = img.shape

        if h < 6:
            st.error("❌ Image is too small to contain a valid message.")
            return

        # Read the message length from the first 4 pixels
        stored_length = sum(img[i, 0, 0] << (i * 8) for i in range(4))

        # Read the password length
        password_length = img[4, 0, 0]
        if password_length + 5 >= h:
            st.error("❌ Corrupted or invalid image format.")
            return

        # Read the stored password
        stored_password = "".join(chr(img[5 + i, 0, 0]) for i in range(password_length))

        if entered_password != stored_password:
            st.error("❌ Incorrect passcode! Access Denied.")
            return

        # Extract the hidden message
        message = ""
        idx = 0
        for row in range(h):
            for col in range(w):
                if row == 0 and col < 5 + password_length:
                    continue
                if idx < stored_length:
                    message += chr(img[row, col, 0])
                    idx += 1
                else:
                    break

        st.success("✅ Decryption Successful!")
        st.text_area("Decrypted Message:", message, height=150)
    except Exception as e:
        st.error(f"❌ Error decoding message: {str(e)}")
