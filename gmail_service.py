# gmail_service.py

import base64
import email
from email import message_from_bytes
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_unread_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_id = msg['id']
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        raw_data = base64.urlsafe_b64decode(msg_data['raw'].encode('ASCII'))
        mime_msg = message_from_bytes(raw_data)

        subject = mime_msg['subject']
        from_email = mime_msg['from']
        body = ""

        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode(errors='ignore')
                        break
                    except:
                        body = "[Could not decode body]"
        else:
            payload = mime_msg.get_payload(decode=True)
            if payload:
                try:
                    body = payload.decode(errors='ignore')
                except:
                    body = "[Could not decode body]"

        emails.append({
            "sender": from_email,
            "subject": subject,
            "body": body
        })

    return emails

def create_draft(service, user_id, to, subject, message_text):
    message = MIMEText(message_text, "plain")
    message["to"] = to
    message["from"] = user_id
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'message': {'raw': raw}}

    try:
        draft = service.users().drafts().create(userId=user_id, body=body).execute()
        print(f"✅ Draft created: ID {draft['id']}")
        return draft
    except Exception as error:
        print(f"❌ Error creating draft: {error}")
        raise

# Classification logic (optional, but included if you still use it)
job_keywords = ['job', 'hiring', 'resume', 'application', 'cv']
internship_keywords = ['internship', 'trainee', 'training']
promo_keywords = ['sale', 'discount', 'coursera', 'newsletter']

def classify_email(subject, body, model=None):
    text = (subject + " " + body).lower()

    if any(word in text for word in job_keywords):
        return "Job"
    elif any(word in text for word in internship_keywords):
        return "Internship"
    elif any(word in text for word in promo_keywords):
        return "Promotional"
    elif model:
        prompt = f"""Classify the following email into one of: Job, Internship, Promotional, Spam, Other:
Subject: {subject}
Body: {body}
Category:"""
        return model(prompt).strip()

    return "Other"
