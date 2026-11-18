"""
Groq LLM Chat — a Streamlit app for Streamlit Community Cloud.

The API key comes from Streamlit secrets (GROQ_API_KEY) or, as a fallback,
from a password box in the sidebar.
"""

import os

import streamlit as st
from groq import Groq

st.set_page_config(page_title="Groq LLM Chat", page_icon="⚡", layout="wide")

# Used only if the live model list can't be fetched.
FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
]

# ---------- API key ----------
def get_api_key() -> str | None:
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass  # no secrets.toml locally
    return os.getenv("GROQ_API_KEY")


api_key = get_api_key()

with st.sidebar:
    st.title("⚡ Groq LLM Chat")
    if not api_key:
        api_key = st.text_input(
            "Groq API key",
            type="password",
            help="Get one free at https://console.groq.com/keys",
        )
    if not api_key:
        st.info("Add your Groq API key to start chatting.")
        st.stop()

client = Groq(api_key=api_key)


# ---------- Models ----------
@st.cache_data(ttl=3600, show_spinner=False)
def list_chat_models(_key_marker: str) -> list[str]:
    """Fetch currently available chat models from Groq (cached for 1 hour)."""
    try:
        models = Groq(api_key=api_key).models.list().data
        skip = ("whisper", "tts", "guard", "embed", "playai")
        ids = sorted(
            m.id for m in models
            if getattr(m, "active", True) and not any(s in m.id.lower() for s in skip)
        )
        return ids or FALLBACK_MODELS
    except Exception:
        return FALLBACK_MODELS


models = list_chat_models(api_key[-6:])
default_idx = models.index("llama-3.3-70b-versatile") if "llama-3.3-70b-versatile" in models else 0

with st.sidebar:
    model = st.selectbox("Model", models, index=default_idx)
    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful, concise assistant.",
        height=100,
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max output tokens", 64, 8192, 1024, 64)
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("Powered by Groq · Built with Streamlit")

# ---------- Chat ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.header(f"Chat with `{model}`")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def stream_reply(messages):
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


if prompt := st.chat_input("Ask me anything…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply(payload))
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Groq API error: {e}")
