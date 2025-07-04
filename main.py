# main.py

from gmail_service import get_service, get_unread_emails, create_draft, classify_email

from Responder_Agent import generate_reply


def main():
    print("\U0001F4EC Authenticating with Gmail...")
    service = get_service()

    print("\U0001F50D Fetching unread emails...")
    emails = get_unread_emails(service)

    if not emails:
        print("✅ No unread emails found.")
        return

    print(f"\U0001F4E8 {len(emails)} unread email(s) found.\n")

    for i, (sender, subject, body) in enumerate(emails, start=1):
        full_text = (subject + " " + body).lower()
        sender_lower = sender.lower()

        relevant_keywords = [
            "internship", "internee",
            "ai developer", "artificial intelligence",
            "chatbot developer", "python developer"
        ]

        skip_keywords = [
            "noreply", "no-reply", "alerts", "job alert", "newsletter", "marketing", "notification"
        ]

        if any(skip in sender_lower for skip in skip_keywords):
            print(f"⏩ Skipping Email #{i} — generic/no-reply sender.")
            continue

        if not any(word in full_text for word in relevant_keywords):
            print(f"⏩ Skipping Email #{i} — not an internship/job of interest.")
            continue

        print(f"--- Email #{i} ---")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print("Generating reply...\n")

        reply = generate_reply(subject, body)

        print("✉️ Suggested Reply:\n")
        print(reply)
        print("\n" + "-" * 26 + "\n")

        # ✅ Auto-save as draft
        try:
            create_draft(service, 'me', sender, f"Re: {subject}", reply)
            print("\U0001F4BE Draft saved successfully!\n")
        except Exception as e:
            print(f"❌ Failed to save draft: {e}\n")


if __name__ == "__main__":
    main()
