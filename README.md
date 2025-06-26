
# ⚖️ Legibly.AI – AI Legal Language Simplifier

> A powerful, multilingual legal clause simplifier built using **Ollama + Mistral**, with risk flagging, voice input/output, OCR, clause comparison, and downloadable reports – all in a clean Streamlit interface.

---

## 🚀 Project Overview

Legal documents are often hard to understand. Legibly.AI helps users (especially non-lawyers) to:

✅ Simplify legal documents (contracts, policies, agreements)  
✅ Understand risk levels in each clause  
✅ Translate simplified text into native languages  
✅ Compare original and simplified clauses side-by-side  
✅ Speak or upload files for analysis  
✅ Download a report of all simplified clauses

---

## 🧠 Core Features

| Feature | Description |
|--------|-------------|
| 📄 Upload Legal Text | Accepts `.txt`, `.pdf`, `.png`, `.jpg`, or typed/pasted content |
| 🧠 Clause Simplifier | Uses Ollama + Mistral to rewrite in plain language |
| 📝 Explanation Generator | Explains legalese in simple terms |
| 🚩 Risk Flagging | Identifies risk level (🔴 High, 🟠 Medium, 🟢 Low) |
| 🌐 Multilingual Output | Translates simplified output into Hindi, Telugu, Spanish, etc. |
| 🗣️ Voice Input | Dictate a clause using mic |
| 🔊 Text-to-Speech | Read back simplified output aloud |
| 📊 Risk Summary Chart | Pie chart of total high/medium/low risk items |
| 🆚 Clause Comparison | View original vs simplified clause side-by-side |
| 📥 Report Download | Export clause-wise report with all outputs |

---

## 🧰 Tech Stack

| Layer | Tech Used |
|-------|-----------|
| 🧠 AI Model | [Ollama](https://ollama.com) running `Mistral` |
| 🧱 Backend | Python |
| 🖥️ UI | Streamlit |
| 📄 OCR | pdfplumber, pytesseract |
| 🗣️ Voice Input | SpeechRecognition + PyAudio |
| 🔊 TTS | pyttsx3 |
| 🌍 Translation | googletrans (fallback) |
| 📊 Charts | Matplotlib |
| 🧠 Prompt Management | Custom prompt templates per task |
| 🗃 Vector Memory *(optional)* | (Pluggable later) |

---

## 📦 Project Structure

```
legal-language-simplifier/
├── app.py                        # Main Streamlit app
├── prompts/                     # Contains text prompt templates
│   ├── simplify.txt
│   ├── explain.txt
│   └── risk_flag.txt
├── utils/
│   └── mistral_runner.py        # Runs LLM + Translation
├── .streamlit/
│   └── config.toml              # Custom theme
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup Instructions

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/your-username/legal-language-simplifier.git
cd legal-language-simplifier
```

### ✅ 2. Create & Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux
```

### ✅ 3. Install Requirements

```bash
pip install -r requirements.txt
```

### ✅ 4. Start Ollama with Mistral

Make sure [Ollama](https://ollama.com) is installed and running:

```bash
ollama run mistral
```

### ✅ 5. Run the App

```bash
streamlit run app.py
```

---

## 📌 Notes

- Ensure `Tesseract` is installed and available in your system PATH for OCR. [Install Tesseract](https://github.com/tesseract-ocr/tesseract)
- For voice features, make sure your microphone works and PyAudio is installed:
```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🧪 Demo Walkthrough

1. 🧾 Upload a PDF, image, or paste legal text  
2. 🧠 It splits the document into clauses  
3. Each clause is:
   - Simplified using Mistral
   - Explained in simple terms
   - Risk-analyzed (with level)  
4. 🎙️ You can speak or hear each clause  
5. 📊 View a chart of risk distribution  
6. 🆚 Compare original vs simplified  
7. 📥 Download a full report

---

## 🧩 Optional Add-ons (Post MVP)

| Add-On | Description | Stack |
|--------|-------------|-------|
| 🗣️ Whisper STT | Use OpenAI Whisper for better voice input | `whisper` |
| 📄 PDF Report Export | Generate stylized PDF | `WeasyPrint`, `pdfkit` |
| 📚 Vector Memory | Save past docs and allow search | `FAISS`, `ChromaDB` |
| 📩 Email Integration | Email the report directly | `smtplib`, `SendGrid` |

---

## 💡 Future Ideas

- Smart highlighting of red-flag clauses
- Legal chatbot (FAQ-based)
- Browser extension for web policies
- Custom contract types (rental, employment, etc.)

---

## 🙌 Team & Credits

- 🧑‍💻 Developer: [Your Name]
- 🤖 LLM Prompting & Strategy: ChatGPT + You
- 🧠 Model: Mistral via Ollama
- 🔊 Voice Tools: Open Source

---

## 📜 License

MIT License. Free for non-commercial use.

---

## 📣 If You Like It...

- ⭐ Star the repo
- 🧠 Use it in your next hackathon or project
- 🤝 Collaborate to build an open legal translator for everyone!
