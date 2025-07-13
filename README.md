# 🧠 AIVA – AI Mental Wellness Assistant

AIVA is a Streamlit-based mental health assistant that enables users to check in on their emotional well-being, chat with a supportive AI, and complete a free-text PHQ-9 assessment — all while preserving privacy and security through Google OAuth login.

---

## 🌟 Features

- 🔐 **Google OAuth Login** for secure access
- 💬 **Chatbot (AIVA)** powered by `DeepSeek-V3`
- 😊 **Mood Journal** with emoji-based check-ins and personal notes
- 📈 **Mood Trends** with bar charts from historical entries
- 📝 **Free-text PHQ-9 Assessment** analyzed by an open-source LLM
- 📞 **Support & Referrals** to mental health helplines and resources
- 🧠 **Open-Source & Private** — data stored locally via SQLite

---

## 🚀 Deployment (Streamlit Cloud)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/aiva-wellness-assistant.git
cd aiva-wellness-assistant
```

### 2. Create `.env` or use Streamlit Cloud Secrets

#### `.env.example`

```env
TOGETHER_API_KEY=your_together_ai_key
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_client_secret
REDIRECT_URI=https://your-app-name.streamlit.app
```

Or on **Streamlit Cloud**, go to:
> ⚙️ Manage App → 🔐 Secrets

And paste the above keys into the secrets editor.

### 3. Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) for frontend
- [Together.ai](https://www.together.ai) + `DeepSeek-V3` for response generation
- [streamlit-oauth](https://github.com/streamlit/streamlit-oauth) for Google login
- [SQLite3](https://www.sqlite.org/) for journaling
- [pandas, requests, dotenv](https://pypi.org) for processing

---

## 🔐 Security & Privacy

- No user data is sent to third-party services beyond Google OAuth
- All mood entries are stored **locally** using SQLite
- No tracking, advertising, or analytics included

---

## 📞 Support Resources

- **iCall**: 9152987821
- **AASRA**: 91-9820466726
- [Tele-MANAS](https://telemanas.mohfw.gov.in/)
- [Practo Mental Health](https://www.practo.com/consult)

---

## 📃 License

MIT License — feel free to fork, modify, and use for non-commercial purposes.

---

## 💡 Inspiration

This project was built to make mental health tools more accessible, customizable, and respectful of user privacy. ✨

## Check it out here !

[AIVA](https://moodcheckai.streamlit.app/)
