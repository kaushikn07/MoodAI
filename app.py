import streamlit as st
from textblob import TextBlob
import emoji
import json
import datetime
from streamlit_option_menu import option_menu

st.set_page_config(page_title="AI Mental Wellness Assistant", layout="wide")

# ---------------------------- Helper Functions ----------------------------
# Mapping emoji to mood labels
MOOD_LABELS = {
    "😄": "happy",
    "🙂": "calm",
    "😐": "neutral",
    "😟": "worried",
    "😢": "sad",
    "😡": "angry"
}


def save_mood_log(mood_emoji, note):
    mood_text = MOOD_LABELS.get(mood_emoji, "unknown")
    log = {"date": str(datetime.datetime.now()), "mood": mood_text, "note": note}

    try:
        with open("mood_log.json", "r") as f:
            content = f.read().strip()
            data = json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(log)

    with open("mood_log.json", "w") as f:
        json.dump(data, f, indent=2)


def score_assessment(answers):
    return sum(answers)

# ---------------------------- Sidebar Navigation ----------------------------

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Welcome", "Chatbot", "Mood Check-In", "Assessment", "Referrals"],
        icons=["house", "chat", "emoji-smile", "clipboard-check", "telephone"],
        menu_icon="person-bounding-box",
        default_index=0,
    )

# ---------------------------- Pages ----------------------------

# 1. Welcome Page
if selected == "Welcome":
    st.title("🧠 AI Mental Wellness Assistant")
    st.markdown("Welcome to your personal mental wellness companion.")
    st.markdown("Please check the box below to continue.")
    if st.checkbox("I consent to anonymous use and data storage."):
        st.success("You may now use the assistant via the sidebar.")

# 2. Chatbot Page
elif selected == "Chatbot":
    import openai
    openai.api_key = "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"  # or os.environ["OPENAI_API_KEY"]

    st.title("💬 Talk to Your Wellness Assistant")

    # Initialize chat history if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "system",
                "content": "You are a kind, supportive AI therapist named AIVA. Keep responses short, warm, and reflective. Offer help if needed."
            }
        ]

    # Display chat history
    for msg in st.session_state.chat_history[1:]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AIVA:** {msg['content']}")

    # Use a form to submit messages (avoids session_state errors)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", "")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("AIVA is thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history,
                temperature=0.7
            )

        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # Rerun to display the new message
        st.rerun()



# 3. Mood Check-In Page
elif selected == "Mood Check-In":
    st.title("😊 Mood Check-In")
    mood = st.radio("How are you feeling right now?", ["😄", "🙂", "😐", "😟", "😢", "😡"])
    note = st.text_area("Want to share why?")
    if st.button("Save Mood"):
        save_mood_log(mood, note)
        st.success("Mood saved.")
        if mood in ["😟", "😢", "😡"]:
            st.warning("It seems you're not feeling great. Consider visiting the Assessment or Referrals tab.")

# 4. Assessment Page
elif selected == "Assessment":
    st.title("📝 PHQ-9 Assessment")
    PHQ9 = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself or that you are a failure",
        "Trouble concentrating",
        "Moving or speaking slowly or being fidgety/restless",
        "Thoughts that you'd be better off dead or hurting yourself"
    ]
    scale = ["0 - Not at all", "1 - Several days", "2 - More than half the days", "3 - Nearly every day"]
    
    answers = []
    for i, q in enumerate(PHQ9):
        st.write(f"**Q{i+1}. {q}**")
        ans = st.radio(f"Your Answer for Q{i+1}", scale, key=f"q{i}")
        answers.append(int(ans[0]))
    
    if st.button("Submit Assessment"):
        total = score_assessment(answers)
        st.subheader(f"Your Total Score: {total}/27")
        
        if total <= 4:
            st.success("Minimal Depression")
        elif total <= 9:
            st.info("Mild Depression")
        elif total <= 14:
            st.warning("Moderate Depression")
        elif total <= 19:
            st.error("Moderately Severe Depression")
        else:
            st.error("Severe Depression. Please seek help.")
        
        if answers[8] > 0:
            st.error("⚠️ Suicidal thoughts detected. Referral strongly recommended.")

# 5. Referral Page
elif selected == "Referrals":
    st.title("📞 Help & Referrals")
    st.markdown("Here are some support options available to you:")
    st.markdown("- 📞 **iCall**: 9152987821")
    st.markdown("- 📞 **AASRA**: 91-9820466726")
    st.markdown("- 🌐 [Tele-MANAS](https://telemanas.mohfw.gov.in/)")
    st.markdown("- 🌐 [Practo - Consult a Therapist](https://www.practo.com/consult)")
    st.markdown("Your well-being matters. Don’t hesitate to seek help.")
