# Detection AI

A Streamlit app that converts plain English detection use cases into YAML rules using the Mixtral-8x7B model via OpenRouter API.

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Running Locally

```bash
streamlit run app.py
```

## Deployment

This app can be deployed for free on Streamlit Community Cloud:

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select this repository
6. Set the main file path to `app.py`
7. Add your OpenRouter API key in the secrets management section 