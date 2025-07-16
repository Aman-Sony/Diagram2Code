# llm/openai_client.py

import openai

# ✅ Using Option 2: Hardcoded API key
openai.api_key = "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"

def generate_code_with_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Python developer who writes clean, working code based on user instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ OpenAI error: {str(e)}"
