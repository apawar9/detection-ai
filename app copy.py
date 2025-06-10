import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

with open("prompts/rulegen.txt", "r") as f:
    PROMPT_TEMPLATE = f.read()

def generate_prompt(use_case):
    return PROMPT_TEMPLATE.replace("{{USE_CASE}}", use_case)

def query_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# UI
st.set_page_config(page_title="Sigma Rule Generator", layout="centered")
st.title("🧠 Sigma Rule Generator (via Mixtral API)")
st.markdown("Enter a detection use case in plain English. Output: Sigma YAML rule.")

use_case = st.text_area("Detection Use Case", height=200)

if st.button("Generate Rule"):
    with st.spinner("Querying Mixtral on OpenRouter..."):
        prompt = generate_prompt(use_case)
        output = query_openrouter(prompt)
        st.code(output.strip(), language="yaml")
