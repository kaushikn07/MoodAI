import streamlit as st
from streamlit_option_menu import option_menu
from openai import OpenAI
import os

# Load from .env if local
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

# Get API key securely
API_KEY = st.secrets["openai"]["api_key"] if "openai" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# -------------- Sidebar Navigation --------------
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Welcome", "Chatbot"],
        icons=["house", "chat"],
        default_index=1,
    )

# -------------- Chatbot Page --------------
if selected == "Chatbot":
    st.title("💬 Talk to Your Wellness Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a kind, supportive AI therapist named AIVA. Keep responses short, warm, and reflective. Offer help if needed."}
        ]

    # Display chat
    for msg in st.session_state.chat_history[1:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AIVA:** {msg['content']}")

    # Form input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("AIVA is thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history,
                temperature=0.7,
            )
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# -------------- Welcome Page --------------
elif selected == "Welcome":
    st.title("🧠 AI Mental Wellness Assistant")
    st.markdown("Welcome to your personal mental wellness chatbot powered by ChatGPT.")
