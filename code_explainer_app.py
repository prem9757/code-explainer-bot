import streamlit as st
import openai
from gtts import gTTS
import os
import base64

# Set your OpenAI API key
openai.api_key = "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"

# Function to explain code using OpenAI
def explain_code(code):
    prompt = f"""You are a helpful programming assistant. Explain what the following Python code does in simple terms:\n\n{code}\n\nExplanation:"""
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400,
    )
    return response['choices'][0]['message']['content'].strip()

# Text-to-speech function
def text_to_speech(text, filename="explanation.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

# Voice download utility
def get_audio_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="explanation.mp3">🔊 Download Audio</a>'

# Streamlit UI
st.set_page_config(page_title="Code Explainer Bot", layout="centered")
st.title("🧠 Code Explainer Bot")
st.markdown("Explain Python code using OpenAI GPT")

uploaded_file = st.file_uploader("Upload a Python (.py) or text file", type=["py", "txt"])
default_code = """for i in range(5):\n    print(i * i)"""

code_input = ""

if uploaded_file:
    code_input = uploaded_file.read().decode("utf-8")
else:
    code_input = st.text_area("Or paste your code below:", height=200, value=default_code)

if st.button("🧠 Explain Code"):
    if code_input.strip() == "":
        st.warning("Please provide some Python code.")
    else:
        with st.spinner("Analyzing your code..."):
            explanation = explain_code(code_input)
        st.subheader("📘 Explanation:")
        st.success(explanation)

        # Voice output
        audio_file = text_to_speech(explanation)
        st.markdown(get_audio_download_link(audio_file), unsafe_allow_html=True)
        st.audio(audio_file, format="audio/mp3")

# Code display with syntax highlighting
if code_input:
    st.subheader("📄 Your Code:")
    st.code(code_input, language="python")
