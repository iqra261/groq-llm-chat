# ⚡ Groq LLM Chat (Streamlit)

A chat app that runs open LLMs (Llama, GPT-OSS, etc.) on Groq, hosted free on Streamlit Community Cloud.

**Features:** live model list from Groq, streaming replies, chat history, editable system prompt, temperature and max-token controls.

## 1. Get a Groq API key
Sign up at https://console.groq.com → **API Keys** → **Create API Key**. Copy the key (starts with `gsk_`).

## 2. Run locally (optional)
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then paste your key
streamlit run app.py
```

## 3. Push to GitHub
```bash
git init
git add .
git commit -m "Groq LLM chat app"
git branch -M main
git remote add origin https://github.com/<your-username>/groq-chat.git
git push -u origin main
```
`.gitignore` keeps `secrets.toml` out of the repo.

## 4. Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Pick your repo, branch `main`, main file `app.py`.
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```
5. Click **Deploy**. You'll get a URL like `https://<your-app>.streamlit.app`.

If you skip the secret, the app asks each visitor for their own key in the sidebar instead.

## Troubleshooting
- **ModuleNotFoundError** → make sure `requirements.txt` is in the repo root.
- **401 / invalid API key** → re-check the secret name is exactly `GROQ_API_KEY`, then reboot the app.
- **Model decommissioned** → just pick another model; the list is fetched live from Groq.
