"""
Email Agent

This module defines the EmailAgent, responsible for sending the final research report
via email using the SendGrid API.

Workflow:
1. Takes a subject and HTML-formatted report body.
2. Uses SendGrid to send the report from a verified sender to a recipient.
3. Returns a simple success response for traceability.

The email-sending function is wrapped as a `function_tool` so it can be invoked by the
agent within the multi-agent orchestration pipeline.
"""

import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

# Tool function exposed to the agent to send an email
@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send an HTML email using SendGrid.

    Args:
        subject (str): The subject line of the email.
        html_body (str): The full HTML content to send.

    Returns:
        dict: A dictionary indicating success.
    """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    
    from_email = Email("ish.mishra03@gmail.com")  # Replace with your verified sender email
    to_email = To("ish.mishra03@gmail.com")        # Replace with your recipient email
    
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()

    response = sg.client.mail.send.post(request_body=mail)
    print("Email response status:", response.status_code)

    return {"status": "success"}

# Natural language instructions to guide the email agent
INSTRUCTIONS = """
You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email,
providing the report converted into clean, well-presented HTML with an appropriate subject line.
"""

# Email agent setup
email_agent = Agent(
    name="EmailAgent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
