import cv2
import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO

def encode_message(image, message, password):
    try:
        img = np.array(image.convert("RGB"))
        h, w, _ = img.shape
        
        if len(message) + len(password) + 5 > h * w:
            st.error("❌ Message is too long to be hidden in this image.")
            return
        
        # Store message length in the first 4 pixels
        for i in range(4):
            img[i, 0, 0] = (len(message) >> (i * 8)) & 0xFF
        
        # Store password length in the 5th pixel
        img[4, 0, 0] = len(password)
        
        # Store password
        for i, char in enumerate(password):
            img[5 + i, 0, 0] = ord(char)
        
        # Store the message
        idx = 0
        for row in range(h):
            for col in range(w):
                if row == 0 and col < 5 + len(password):
                    continue
                if idx < len(message):
                    img[row, col, 0] = ord(message[idx])
                    idx += 1
                else:
                    break
        
        encoded_image = Image.fromarray(img)
        buf = BytesIO()
        encoded_image.save(buf, format="PNG")
        st.success("✅ Message encoded successfully! Download below:")
        st.download_button("Download Encoded Image", buf.getvalue(), "encoded_image.png", "image/png")
    except Exception as e:
        st.error(f"❌ Error encoding message: {str(e)}")