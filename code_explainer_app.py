import streamlit as st
import openai
from gtts import gTTS
import os
import base64

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"

# Create OpenAI client (for openai>=1.0.0)
client = openai.OpenAI(api_key=openai_api_key)

# Function to explain code
def explain_code(code):
    prompt = f"""You are a helpful programming assistant. Explain what the following Python code does in simple terms:\n\n{code}\n\nExplanation:"""
    
    response = client.chat.completions.create(
        model="gpt-4",  # Or gpt-3.5-turbo
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )

    return response.choices[0].message.content.strip()

# Function to convert text to speech
def text_to_speech(text, filename="explanation.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

# Generate download link for audio
def get_audio_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="explanation.mp3">🔊 Download Audio</a>'

# Streamlit app
st.set_page_config(page_title="🧠 Code Explainer Bot", layout="centered")
st.title("🧠 Code Explainer Bot")
st.markdown("Upload or paste Python code to get a clear explanation using GPT-4.")

# File uploader
uploaded_file = st.file_uploader("📂 Upload a .py or .txt file", type=["py", "txt"])
default_code = "for i in range(5):\n    print(i * i)"
code_input = ""

if uploaded_file:
    code_input = uploaded_file.read().decode("utf-8")
else:
    code_input = st.text_area("Or paste your Python code below:", height=200, value=default_code)

# Run explanation
if st.button("🧠 Explain Code"):
    if code_input.strip() == "":
        st.warning("⚠️ Please provide some Python code.")
    else:
        with st.spinner("Analyzing your code with GPT-4..."):
            try:
                explanation = explain_code(code_input)
                st.subheader("📘 Explanation:")
                st.success(explanation)

                audio_file = text_to_speech(explanation)
                st.markdown(get_audio_download_link(audio_file), unsafe_allow_html=True)
                st.audio(audio_file, format="audio/mp3")

            except Exception as e:
                st.error(f"Error: {e}")

# Display code
if code_input:
    st.subheader("📄 Your Code:")
    st.code(code_input, language="python")
