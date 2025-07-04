# 📬 AI-Powered Gmail Auto-Responder (Agentic AI Project)

An intelligent email assistant that automatically:
- Connects to your Gmail account,
- Filters job & internship emails,
- Skips newsletters or irrelevant content,
- Generates smart replies using an LLM (Gemma 2B via Ollama),
- And saves them as Gmail drafts — all through a simple UI!

---

## 🚀 Features

✅ Real-time Gmail integration using Gmail API  
✅ OAuth2.0 login for secure access  
✅ AI classification of emails: Job / Internship / Promotional  
✅ LLM-based response generation (Ollama + Gemma 2B)  
✅ One-click draft saving  
✅ Beautiful Streamlit dashboard for interaction  
✅ Skips irrelevant content automatically  

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – interactive dashboard
- **Gmail API** – fetch & draft emails
- **Ollama** – local LLM interface
- **Gemma 2B** – used as reasoning model
- **OAuth 2.0** – Gmail authentication

---

## 🧠 Agentic Flow

1. Login with Gmail using OAuth  
2. Fetch all unread emails  
3. Filter relevant messages based on job/internship keywords  
4. Generate a custom reply using LLM  
5. Save reply as Gmail draft  
6. Skip and move to the next email automatically

---

## 🔐 Setup
clone the repo
pip install -r requirements.txt
streamlit run app.py


🧠 What Inspired This?
I wanted to automate my daily workflow and build a real-world AI agent.
This project showcases how LLMs + APIs can reduce decision fatigue and enhance productivity.

🙌 Contributing
Pull requests welcome. Let's build more AI agents that save real-world time!

📄 License
MIT License
