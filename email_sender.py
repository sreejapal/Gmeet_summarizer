import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_summary_email(receiver_email, summary):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError(
            "Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your .env file. "
            "For Gmail, use an App Password: https://myaccount.google.com/apppasswords"
        )

    yag = yagmail.SMTP(
        EMAIL_ADDRESS,
        EMAIL_PASSWORD
    )

    body = f"""
MEETING SUMMARY

Overview:
{summary.get("overview", "")}

Discussion Points:
{chr(10).join(summary.get("discussion_points", []))}

Action Items:
{chr(10).join(summary.get("action_items", []))}

Decisions:
{chr(10).join(summary.get("decisions", []))}

Task Assignments:
{chr(10).join(summary.get("task_assignments", []))}

Next Steps:
{chr(10).join(summary.get("next_steps", []))}
"""

    yag.send(
        to=receiver_email,
        subject="Meeting Summary",
        contents=body
    )