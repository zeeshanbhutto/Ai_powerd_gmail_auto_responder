import streamlit as st
from gmail_service import get_service, get_unread_emails, create_draft, classify_email
from Responder_Agent import generate_reply
from ollama import Client

# Initialize LLM model
model = Client().chat

# App UI setup
st.set_page_config(page_title="Email AI Auto-Responder", layout="wide")
st.title("📬 AI-Powered Email Auto-Responder")
st.markdown("This tool reads your unread emails and generates intelligent replies. You decide which ones to approve and save as drafts.")

# Session state initialization
if "emails" not in st.session_state:
    st.session_state.emails = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# Fetch button
if st.button("🔍 Fetch Unread Emails"):
    service = get_service()
    st.session_state.emails = get_unread_emails(service)
    st.session_state.current_index = 0
    if not st.session_state.emails:
        st.success("✅ No unread emails found.")

# Show current email logic
if st.session_state.emails:
    i = st.session_state.current_index
    if i < len(st.session_state.emails):
        email = st.session_state.emails[i]
        sender = email.get("sender", "")
        subject = email.get("subject", "")
        body = email.get("body", "")

        full_text = (subject + " " + body).lower()
        sender_lower = sender.lower()

        # Keyword-based filtering
        relevant_keywords = ["internship", "internee", "ai developer", "chatbot developer", "python developer"]
        skip_keywords = ["noreply", "no-reply", "alerts", "job alert", "newsletter", "marketing", "notification"]

        # Skip conditions
        if any(skip in sender_lower for skip in skip_keywords):
            st.info(f"⛔ Skipped Email #{i+1}: Detected as promotional or system-generated ({sender})")
        elif not any(word in full_text for word in relevant_keywords):
            st.info(f"⛔ Skipped Email #{i+1}: Not relevant to jobs/internships.")
        else:
            st.markdown(f"**📨 Email #{i+1}**")
            st.markdown(f"**From:** {sender}")
            st.markdown(f"**Subject:** {subject}")
            st.markdown(f"**Body:**\n\n{body}")

            reply = generate_reply(subject, body)
            st.text_area("✉️ Suggested Reply", reply, height=200, key=f"reply_{i}")

            if st.button(f"💾 Approve & Save Draft #{i+1}", key=f"save_{i}"):
                try:
                    service = get_service()
                    create_draft(service, 'me', sender, f"Re: {subject}", reply)
                    st.success("✅ Draft saved successfully!")
                except Exception as e:
                    st.error(f"❌ Error saving draft: {e}")

        # Button to move to next email
        if st.button("➡️ Next Email"):
            st.session_state.current_index += 1
    else:
        st.success("🎉 You've reviewed all unread emails.")
