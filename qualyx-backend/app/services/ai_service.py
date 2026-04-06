# app/services/ai_service.py
import json
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

EXTRACTION_PROMPT = '''
You are a lead extraction AI for B2B sales.
Given a raw message, extract these fields as JSON:
name, email, phone, company, interest, budget, urgency (high/medium/low), notes
Return ONLY valid JSON. No markdown, no explanation.
Example: {"name": "Raj Patel", "email": "raj@co.in", "phone": "+91-9876543210", "company": "Co", "interest": "CRM", "budget": "10000", "urgency": "high", "notes": ""}
'''

QUALIFICATION_PROMPT = '''
Score this lead 0-100 and classify as hot/warm/cold:
HOT (75-100): clear need + budget + urgency, decision maker
WARM (40-74): has need, needs nurturing
COLD (0-39): vague need, no budget, just exploring
Return ONLY: {"score": 82, "qualification": "hot", "reasoning": "...one sentence"}
'''

async def extract_lead(raw_text: str) -> dict:
    prompt = f'{EXTRACTION_PROMPT}\n\nRaw: "{raw_text}"'
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    text = response.text.strip().replace('```json', '').replace('```', '')
    return json.loads(text)

async def qualify_lead(lead_data: dict) -> dict:
    summary = json.dumps({
        'interest': lead_data.get('interest'),
        'budget':   lead_data.get('budget'),
        'urgency':  lead_data.get('urgency'),
        'company':  lead_data.get('company'),
    })
    prompt = f'{QUALIFICATION_PROMPT}\n\nLead: {summary}'
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    text = response.text.strip().replace('```json', '').replace('```', '')
    result = json.loads(text)
    result['score'] = max(0, min(100, int(result.get('score', 0))))
    return result

async def generate_email(lead: dict) -> dict:
    prompt = f'''Write a personalized sales email for:
    Name: {lead['name']}, Company: {lead.get('company','')},
    Interest: {lead.get('interest','')}, Score: {lead.get('score',0)}/100
    Keep under 120 words. Return JSON: {{"subject": "...", "body": "..."}}'''
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    text = response.text.strip().replace('```json', '').replace('```', '')
    return json.loads(text)