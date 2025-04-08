import streamlit as st
import os
from PIL import Image
import json

# Directory and files
IMAGE_DIR = "images"
LIKES_FILE = "likes.json"

# Get image files
image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))])

# Load likes from JSON or initialize
def load_likes():
    if os.path.exists(LIKES_FILE):
        with open(LIKES_FILE, "r") as f:
            return json.load(f)
    else:
        return {img: 0 for img in image_files}

# Save likes to JSON
def save_likes(likes):
    with open(LIKES_FILE, "w") as f:
        json.dump(likes, f)

# Session state init
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'likes' not in st.session_state:
    st.session_state.likes = load_likes()

# UI Title
st.title("📷 Image Rating App")

if image_files:
    current_index = st.session_state.index
    current_img = image_files[current_index]

    # Show image full width
    image_path = os.path.join(IMAGE_DIR, current_img)
    image = Image.open(image_path)
    st.image(image, caption=current_img, use_container_width=True)

    # Show like count
    st.markdown(f"<div style='text-align: center; font-size: 18px;'>👍 <strong>Likes: {st.session_state.likes[current_img]}</strong></div>", unsafe_allow_html=True)

    # Buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous"):
            if current_index > 0:
                st.session_state.index -= 1

    with col2:
        if st.button("👍 Thumbs Up"):
            st.session_state.likes[current_img] += 1
            save_likes(st.session_state.likes)
            st.success("You liked this image!")

    with col3:
        if st.button("➡️ Next"):
            if current_index < len(image_files) - 1:
                st.session_state.index += 1

    # Optional: Summary
    with st.expander("📊 Likes Summary"):
        for img in image_files:
            st.write(f"- {img}: {st.session_state.likes[img]} 👍")

else:
    st.error("No images found in the 'images/' folder.")
