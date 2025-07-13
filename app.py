# AI Mental Wellness Assistant - Google OAuth Version

import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from datetime import datetime
import os
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv
import requests
from collections import Counter
import pandas as pd

# ------------------------ Environment Setup ------------------------
if os.path.exists(".env"):
    load_dotenv()

# ------------------------ Together.ai Model Config ------------------------
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
MODEL_NAME = "deepseek-ai/DeepSeek-V3"
headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}
API_URL = "https://api.together.xyz/v1/chat/completions"

def generate_response(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.7
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠️ Sorry, the assistant is currently unavailable."

# ------------------------ SQLite Init ------------------------
conn = sqlite3.connect("mood_logs.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS moods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        mood TEXT,
        note TEXT,
        timestamp TEXT
    )
""")
conn.commit()

# ------------------------ Google OAuth Setup ------------------------
client_id = st.secrets["GOOGLE_CLIENT_ID"]
client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
redirect_uri = st.secrets["REDIRECT_URI"]
if not redirect_uri:
    st.stop()

oauth = OAuth2Component(
    client_id=client_id,
    client_secret=client_secret,
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token"
)

# ------------------------ Pages ------------------------
def chatbot_page():
    st.title("💬 Chat with AIVA")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "system", "content": "You are a supportive AI wellness therapist named AIVA."}
        ]

    for msg in st.session_state.chat_history[1:]:
        st.markdown(f"**{'You' if msg['role']=='user' else 'AIVA'}:** {msg['content']}")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("AIVA is thinking..."):
            reply = generate_response(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

def mood_checkin_page():
    st.title("😊 Mood Check-In")
    mood = st.radio("How are you feeling?", ["happy", "calm", "neutral", "worried", "sad", "angry"])
    note = st.text_area("Want to elaborate?")
    if st.button("Save Mood"):
        cursor.execute("INSERT INTO moods (email, mood, note, timestamp) VALUES (?, ?, ?, ?)",
                       (st.session_state.user_email, mood, note, str(datetime.now())))
        conn.commit()
        st.success("Mood saved")

    st.subheader("Your Past Mood Entries")
    cursor.execute("SELECT mood, note, timestamp FROM moods WHERE email = ? ORDER BY timestamp DESC", (st.session_state.user_email,))
    entries = cursor.fetchall()

    emoji_map = {
        "happy": "😊",
        "calm": "😌",
        "neutral": "😐",
        "worried": "😟",
        "sad": "😢",
        "angry": "😠"
    }

    for mood, note, timestamp in entries:
        dt = datetime.strptime(timestamp[:19], "%Y-%m-%d %H:%M:%S")
        formatted_time = dt.strftime("%d %B %Y, %I:%M %p").replace(" 0", " ")
        mood_emoji = emoji_map.get(mood, "")
        st.markdown(f"**{formatted_time}** - {mood_emoji} {mood.capitalize()}  ")
        if note:
            st.markdown(f"> {note}")

    st.subheader("📈 Mood Trend")
    mood_counts = Counter([entry[0] for entry in entries])
    if mood_counts:
        df = pd.DataFrame.from_dict(mood_counts, orient="index", columns=["Count"]).reset_index()
        df.columns = ["Mood", "Count"]
        st.bar_chart(df.set_index("Mood"))

def assessment_page():
    st.title("📝 PHQ-9 Assessment (Free Text)")
    PHQ9 = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble sleeping",
        "Feeling tired or low energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself",
        "Trouble concentrating",
        "Restlessness or slowness",
        "Thoughts of self-harm"
    ]
    answers = []
    for i, q in enumerate(PHQ9):
        ans = st.text_area(f"Q{i+1}: {q}")
        answers.append(f"Q{i+1}: {q}\nAnswer: {ans}\n")

    if st.button("Analyze My Answers"):
        full_prompt = "You are a mental health expert. Based on the following answers to PHQ-9, summarize the user's state of mind and give gentle, actionable advice.\n\n" + "\n".join(answers)
        with st.spinner("Analyzing your answers..."):
            reply = generate_response([
                {"role": "system", "content": "You are a compassionate mental health advisor."},
                {"role": "user", "content": full_prompt}
            ])
        st.markdown("### 🧠 Insight from AIVA")
        st.write(reply)

def referral_page():
    st.title("📞 Support & Referrals")
    st.markdown("- **iCall**: 9152987821")
    st.markdown("- **AASRA**: 91-9820466726")
    st.markdown("- [Tele-MANAS](https://telemanas.mohfw.gov.in/)")
    st.markdown("- [Practo - Mental Health](https://www.practo.com/consult)")

# ------------------------ Main App ------------------------
st.set_page_config(page_title="AIVA - Mental Wellness Assistant", page_icon="🧠")

def main():
    

    if "user_email" not in st.session_state:
        st.markdown("""
            <div style='text-align: center; margin-top: 20%;'>
                <h2>🧠 Welcome to AIVA</h2>
                <p>Please log in with Google to continue.</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            token = oauth.authorize_button(
                "🔐 Login with Google",
                redirect_uri=redirect_uri,
                scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
            )

        if token:
            headers_ = {"Authorization": f"Bearer {token['token']['access_token']}"}
            userinfo = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers_).json()
            if userinfo and userinfo.get("email"):
                st.session_state.user_email = userinfo["email"]
                st.rerun()
            else:
                st.error("Could not retrieve user info. Try again.")
        else:
            return

    st.success(f"✅ Logged in as {st.session_state.user_email}")
    with st.sidebar:
        if st.button("Logout"):
            del st.session_state.user_email
            st.rerun()

        selected = option_menu(
            "Navigation",
            ["Welcome", "Chatbot", "Mood Check-In", "Assessment", "Referrals"],
            icons=["house", "chat", "emoji-smile", "check2-square", "telephone"],
            default_index=0
        )

    if selected == "Welcome":
        st.title("👋 Welcome to the AI Mental Wellness Assistant")
        st.markdown("This app supports your emotional wellbeing. Use the navigation menu to explore.")
    elif selected == "Chatbot":
        chatbot_page()
    elif selected == "Mood Check-In":
        mood_checkin_page()
    elif selected == "Assessment":
        assessment_page()
    elif selected == "Referrals":
        referral_page()

if __name__ == "__main__":
    main()
