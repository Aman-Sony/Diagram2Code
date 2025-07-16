# llm/gemini_client.py

import google.generativeai as genai

# ✅ Replace this with your actual Gemini API key
genai.configure(api_key="AIzaSyAYm3N8YYjecmSxmkCoB-EL9wZq5Qf28cQ")

# ✅ Generate code using Gemini 1.5 Pro Latest
def generate_code_with_gemini(prompt: str, model_name: str = "models/gemini-1.5-pro-latest") -> str:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini error: {str(e)}"

# ✅ List all available models and supported methods
def list_available_gemini_models() -> str:
    try:
        models = genai.list_models()
        output_lines = []
        for m in models:
            methods = ", ".join(m.supported_generation_methods)
            output_lines.append(f"📌 {m.name} → supports: {methods}")
        return "\n".join(output_lines)
    except Exception as e:
        return f"❌ Could not list models: {str(e)}"
