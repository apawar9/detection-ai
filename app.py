import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Try to load from .env file first (local development)
load_dotenv()
# Then try to get from Streamlit secrets (production)
API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets["OPENROUTER_API_KEY"]

# Load prompt template
with open("C:/Users/abhij/OneDrive/Desktop/Detection AI/sigma-rulegen/prompts/rulegen.txt", "r") as f:
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
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

st.set_page_config(page_title="Sigma Rule Generator", layout="centered")
st.title("🧠 Detection AI (via Mixtral API)")
st.markdown("Enter a detection use case in plain English. Output: YAML rule.")

# --- Input for original use case ---
use_case = st.text_area("Detection Use Case", height=200)

# Store rule in session
if "generated_rule" not in st.session_state:
    st.session_state["generated_rule"] = ""

if st.button("Generate Rule"):
    with st.spinner("Querying Mixtral on OpenRouter..."):
        prompt = generate_prompt(use_case)
        output = query_openrouter(prompt)
        st.session_state["generated_rule"] = output.strip()

# Show the generated rule
if st.session_state["generated_rule"]:
    st.subheader("📄 Generated Sigma Rule")
    st.code(st.session_state["generated_rule"], language="yaml")

    # Follow-up section
    st.markdown("### ✏️ Follow-Up Prompt")
    follow_up = st.text_area("Give instructions to tweak the rule (e.g., 'Change logsource to AWS')", height=100)

    if st.button("Apply Follow-Up"):
        with st.spinner("Tweaking the rule..."):
            followup_prompt = f"""You previously generated this Sigma rule:
---
{st.session_state["generated_rule"]}
---

Now modify it with the following instruction:
"{follow_up}"

Only return the updated Sigma rule in YAML format. No explanation."""
            new_output = query_openrouter(followup_prompt)
            st.session_state["generated_rule"] = new_output.strip()
            st.success("Rule updated!")

            # Show new rule
            st.code(st.session_state["generated_rule"], language="yaml")
