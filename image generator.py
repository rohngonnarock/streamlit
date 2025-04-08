import streamlit as st
import openai
from PIL import Image
import io

# Initialize OpenAI client (new SDK style)
client = openai.OpenAI(
    api_key="key")

st.set_page_config(page_title="AI Pattern Generator", layout="centered")
st.title("🎨 AI Pattern Generator Playground")
st.markdown(
    "Upload a reference image, and we'll generate a high-resolution enhanced pattern inspired by it.")

# File uploader
uploaded_file = st.file_uploader(
    "Upload a reference image", type=["jpg", "jpeg", "png"])

# Base prompt
base_prompt = ("A seamless high-definition digital pattern created at 1792x1024 resolution, designed for wallpapers or gift wraps. Style is modern and elegant, in soft pastel tones. "
               "Features clean lines, balanced composition, and subtle textures for depth. Vector-style or hand-drawn aesthetics, suitable for upscale minimalist design, rendered in HD quality.")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Reference Image", use_container_width=True)
    custom_notes = st.text_area(
        "Add anything specific you'd like to enhance or change:", "")
    final_prompt = base_prompt + (" " + custom_notes if custom_notes else "")
else:
    final_prompt = st.text_area(
        "Describe the pattern you want to generate from scratch:")

# Generation button
if st.button("Generate Enhanced Pattern"):
    with st.spinner("Generating pattern with DALL·E 3..."):
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=final_prompt,
                size="1792x1024",
                quality="hd",
                n=1
            )
            image_url = response.data[0].url
            st.image(image_url, caption="Generated Pattern")
            st.markdown(f"[🔗 Download Image]({image_url})")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using OpenAI + Streamlit")
