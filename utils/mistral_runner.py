import subprocess

def run_mistral(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[Error running Mistral]: {str(e)}"

def load_prompt(template_path: str, clause: str) -> str:
    with open(template_path, "r") as file:
        template = file.read()
    return template.replace("{{CLAUSE}}", clause.strip())

from googletrans import Translator
translator = Translator()

def translate_text(text, target_lang):
    lang_map = {
        "Hindi": "hi",
        "Telugu": "te",
        "Spanish": "es",
        "English": "en"
    }
    if target_lang in lang_map:
        return translator.translate(text, dest=lang_map[target_lang]).text
    return text

