import streamlit as st
import os
from PIL import Image

# Directory where your images are stored
IMAGE_DIR = "images"
image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# Initialize session state
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}
if 'likes' not in st.session_state:
    st.session_state.likes = {img: 0 for img in image_files}

# Display current image
def show_image(index):
    image_path = os.path.join(IMAGE_DIR, image_files[index])
    image = Image.open(image_path)
    
    st.image(image, caption=image_files[index], use_container_width=True)
    
    # Show like count
    likes = st.session_state.likes.get(image_files[index], 0)
    st.markdown(f"<div style='text-align: center; font-size: 18px;'>👍 <strong>Likes: {likes}</strong></div>", unsafe_allow_html=True)

# Main UI

if image_files:
    current_img = image_files[st.session_state.index]
    show_image(st.session_state.index)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous"):
            if st.session_state.index > 0:
                st.session_state.index -= 1

    with col2:
        if st.button("👍 Like"):
            st.session_state.likes[current_img] += 1
            st.session_state.ratings[current_img] = "Like"
            st.success("You liked this image!")

    with col3:
        if st.button("➡️ Next"):
            if st.session_state.index < len(image_files) - 1:
                st.session_state.index += 1

    # Optional: show ratings summary
    with st.expander("📊 Your Ratings Summary"):
        for img, rating in st.session_state.ratings.items():
            st.write(f"- {img}: {rating} ({st.session_state.likes[img]} likes)")

else:
    st.error("No images found in the 'images/' folder.")
