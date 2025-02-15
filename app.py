import streamlit as st
import requests
import json
import webbrowser

# Streamlit UI
st.set_page_config(page_title="Screen Text Capture", layout="wide")
st.title("📸 Screen Text Capture")

# Instructions
st.markdown("1. Click **Capture Screen** to open a new tab for screen capture.")
st.markdown("2. Capture your screen, and the extracted text will appear here.")
st.markdown("3. Download the extracted text as a JSON file.")

# Button to trigger screen capture
if st.button("📷 Capture Screen"):
    webbrowser.open_new_tab("http://127.0.0.1:5000/capture")

# Fetch OCR result from backend
if st.button("🔍 Get Extracted Text"):
    response = requests.get("http://127.0.0.1:5000/get_text")
    if response.status_code == 200:
        extracted_text = response.json()
        st.json(extracted_text)
        with open("captured_text.json", "w") as f:
            json.dump(extracted_text, f)
        st.download_button("Download JSON", "captured_text.json", "application/json")
    else:
        st.error("❌ Error fetching text. Try again!")
