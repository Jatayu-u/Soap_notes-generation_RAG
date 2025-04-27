# streamlit_app.py

import streamlit as st
import requests
from PIL import Image

# FastAPI server URL
API_URL = "http://localhost:8000/generate_soap_note"

# Set page configuration for a cleaner look
st.set_page_config(
    page_title="🩺 SOAP Note Generator",
    page_icon="📝",
    layout="wide",
)

# Add custom CSS for a cleaner, modern look
st.markdown(
    """
    <style>
    .stTextArea [data-baseweb="text-area"] {
        border-radius: 10px;
        border: 2px solid #4CAF50;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #4CAF50;
        padding: 10px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #45a049;
    }
    .stTextArea>label {
        font-size: 16px;
        color: #333;
    }
    .stMarkdown {
        font-size: 16px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header with an image and description
st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🩺 SOAP Note Generator</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <h3 style='text-align:center; color:#555;'>Efficiently generate structured SOAP notes from doctor-patient conversations.</h3>
    <p style='text-align:center; color:#777;'>Just input the conversation, and we'll handle the rest! 🚀</p>
    """,
    unsafe_allow_html=True,
)

# Optionally, you could add a logo or image here (replace the URL with your image path)
# logo = Image.open("logo.png")
# st.image(logo, width=200)

# Input area for conversation
conversation = st.text_area(
    "Enter Doctor-Patient Conversation:",
    height=300,
    placeholder="Type or paste the doctor-patient conversation here...",
    label_visibility="collapsed"
)

# Button to trigger SOAP note generation
if st.button("Generate SOAP Note"):
    if not conversation.strip():
        st.error("Please enter a conversation before generating.")
    else:
        with st.spinner("Generating SOAP Note..."):
            try:
                # Send POST request to FastAPI
                response = requests.post(API_URL, json={"conversation": conversation})
                if response.status_code == 200:
                    soap_note = response.json()["soap_note"]
                    st.success("SOAP Note Generated Successfully!")
                    st.text_area("Generated SOAP Note", soap_note, height=400)
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer with a clean message
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; color:#888;'>
        Built by <strong>Shaurya Vats</strong> + <strong>Augnito</strong> | Powered by AI 🧠
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional: Add custom JavaScript or HTML for interactive features (e.g., background image, animations)
