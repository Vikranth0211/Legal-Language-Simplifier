import streamlit as st
import pdfplumber
from PIL import Image
import pytesseract
import os
import speech_recognition as sr
import pyttsx3
import threading
from collections import Counter
import re
import matplotlib.pyplot as plt
import io

from utils.mistral_runner import run_mistral, load_prompt, translate_text

# --- App Configuration ---
st.set_page_config(page_title="Legibly.AI – Legal Language Simplifier", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #3A3A3A;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.image("assets/legal_logo.png", width=80)
st.markdown('<div class="main-title">⚖️ Legibly.AI – Understand What You Sign</div>', unsafe_allow_html=True)
st.caption("An LLM-powered legal translator built using Mistral via Ollama")
st.markdown("---")

# --- TTS Stop Flag ---
tts_stop_flag = {"stop": False}

# --- Clause Splitter ---
def split_into_clauses(text):
    return [clause.strip() for clause in re.split(r'\n{2,}|(?<=\.)\s+(?=\d+\.|\-)', text) if clause.strip()]

# --- Text Extractors ---
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
    return text

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

# --- TTS Function ---
def speak_text(text, stop_flag):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    def on_word(name, location, length):
        if stop_flag["stop"]:
            engine.stop()

    engine.connect('started-word', on_word)
    engine.say(text)
    engine.runAndWait()

# --- Streamlit App ---
st.set_page_config(page_title="Legibly.AI", layout="wide")
st.title("📄 Legal Language Simplifier (Mistral + OCR)")

# Sidebar Language Selector
st.sidebar.header("🌐 Language Settings")
target_lang = st.sidebar.selectbox("Translate simplified version to:", ["None", "English", "Hindi", "Telugu", "Spanish"])

# Upload or Paste Input
uploaded_file = st.file_uploader("Upload a .txt, .pdf, or image file", type=["txt", "pdf", "png", "jpg", "jpeg"])
text_input = st.text_area("Or paste legal text here", height=250)
raw_text = ""

# Voice Input
st.markdown("### 🎤 Voice Input (Speak a Legal Clause)")
if st.button("Start Recording"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now.")
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        st.success(f"You said: {recognized_text}")
        text_input = recognized_text
        raw_text = recognized_text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand your voice.")
    except sr.RequestError as e:
        st.error(f"STT Error: {e}")

# File Upload Handling
if uploaded_file:
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        raw_text = extract_text_from_pdf(uploaded_file)
    elif file_type.startswith("image/"):
        raw_text = extract_text_from_image(uploaded_file)
    elif file_type == "text/plain":
        raw_text = uploaded_file.read().decode("utf-8")

elif text_input:
    raw_text = text_input

# Process and Display Clauses
if raw_text:
    st.subheader("📑 Extracted Text")
    st.text_area("Raw Legal Text", raw_text, height=300)

    clauses = split_into_clauses(raw_text)
    st.subheader("🧠 Full Clause-by-Clause Analysis")

    results = []
    risk_counter = Counter()

    for i, clause in enumerate(clauses, 1):
        with st.expander(f"📄 Clause {i}"):
            st.markdown(f"**Original Clause:**\n\n{clause}")

            with st.spinner("🔄 Processing with Mistral..."):
                simp_prompt = load_prompt("prompts/simplify.txt", clause)
                simplified = run_mistral(simp_prompt)

                explain_prompt = load_prompt("prompts/explain.txt", clause)
                explanation = run_mistral(explain_prompt)

                risk_prompt = load_prompt("prompts/risk_flag.txt", clause)
                risk = run_mistral(risk_prompt)

            # Translate simplified output
            if target_lang != "None" and target_lang != "English":
                simplified_translated = translate_text(simplified, target_lang)
            else:
                simplified_translated = simplified

            # Risk Level Logic
            risk_level = "Low"
            if re.search(r"\bhigh\b", risk.lower()):
                risk_level = "High"
            elif re.search(r"\bmedium\b", risk.lower()):
                risk_level = "Medium"
            elif re.search(r"\blow\b", risk.lower()):
                risk_level = "Low"

            risk_counter[risk_level] += 1
            results.append({
                "clause": clause,
                "simplified": simplified_translated,
                "explanation": explanation,
                "risk": risk,
                "risk_level": risk_level
            })

            # Display Results
            st.markdown("### ✅ Simplified")
            st.success(simplified_translated)

            st.markdown("### 📘 Explanation")
            st.info(explanation)

            st.markdown("### ⚠️ Risk Flag")
            st.warning(f"**Risk Level:** {risk_level}\n\n{risk}")

            # TTS Controls
            col1, col2 = st.columns(2)
            if col1.button(f"🔊 Speak Clause {i}"):
                tts_stop_flag["stop"] = False
                tts_thread = threading.Thread(target=speak_text, args=(simplified_translated, tts_stop_flag))
                tts_thread.start()

            if col2.button(f"🛑 Stop Speaking Clause {i}"):
                tts_stop_flag["stop"] = True


            # Clause Comparator View
            with st.expander("🆚 Compare Clause Versions"):
                st.markdown("**Original Clause:**")
                st.code(clause, language="text")

                st.markdown("**Simplified Clause:**")
                st.code(simplified, language="text")

    # Risk Chart Summary
    if results:
        st.subheader("📊 Risk Summary Chart")
        labels = list(risk_counter.keys())
        values = [risk_counter[l] for l in labels]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=["green", "orange", "red"])
        ax.axis('equal')
        st.pyplot(fig)

    # Download Simplified Report
    if st.button("📥 Download Simplified Report"):
        output = io.StringIO()
        output.write("# Legibly.AI – Simplified Legal Report\n\n")
        for i, item in enumerate(results, 1):
            output.write(f"## Clause {i}\n")
            output.write(f"**Original:** {item['clause']}\n\n")
            output.write(f"**Simplified:** {item['simplified']}\n\n")
            output.write(f"**Explanation:** {item['explanation']}\n\n")
            output.write(f"**Risk Level:** {item['risk_level']}\n\n---\n\n")
        st.download_button("Download as .txt", data=output.getvalue(), file_name="legal_simplified_report.txt")
