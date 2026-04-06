# app/services/email_service.py
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings
from app.services.ai_service import generate_email

async def send_lead_email(lead: dict) -> dict:
    if not lead.get('email'):
        return {'success': False, 'error': 'No email address'}

    # Generate AI personalised content
    content = await generate_email(lead)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = content['subject']
    msg['From']    = f'{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>'
    msg['To']      = lead['email']
    msg.attach(MIMEText(content['body'], 'plain'))
    msg.attach(MIMEText(_wrap_html(lead['name'], content['body']), 'html'))

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASS,
        start_tls=True,
    )
    return {'success': True, 'subject': content['subject']}

def _wrap_html(name, body):
    lines = ''.join(f'<p>{l}</p>' for l in body.split('\n') if l)
    return f'''<html><body style="font-family:Arial;max-width:600px;margin:auto">
    <div style="background:#0F172A;padding:16px 24px">
      <h2 style="color:#06B6D4;margin:0">Qualy<span style="color:#F59E0B">X</span></h2>
    </div>
    <div style="padding:24px">{lines}</div></body></html>'''

