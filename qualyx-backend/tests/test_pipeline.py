import asyncio
from dotenv import load_dotenv

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.services.ai_service import extract_lead, qualify_lead
from app.services.lead_service import create_lead
# ... rest of the file
load_dotenv()

from app.services.ai_service import extract_lead, qualify_lead
from app.services.lead_service import create_lead

async def test_full_pipeline():
    print("\n🚀 Testing Full Pipeline\n")

    # Step 1 - Simulate a raw CSV row
    raw = {
        "name": "Priya Sharma",
        "email": "priya@startup.io",
        "phone": "+91-9876543210",
        "company": "Startup Co",
        "interest": "CRM for 200 clients",
        "budget": "50000",
        "urgency": "high",
        "source": "csv_upload"
    }
    print(f"📥 Raw lead: {raw['name']}")

    # Step 2 - AI Qualification
    print("🤖 Running Gemini qualification...")
    qual = await qualify_lead(raw)
    raw['score'] = qual['score']
    raw['qualification'] = qual['qualification']
    raw['ai_reasoning'] = qual.get('reasoning', '')
    print(f"🎯 Score: {raw['score']} | {raw['qualification'].upper()}")
    print(f"💡 Reasoning: {raw['ai_reasoning']}")

    # Step 3 - Save to Supabase
    print("💾 Saving to Supabase...")
    saved = await create_lead(raw)
    print(f"✅ Saved! ID: {saved['id']}")
    print(f"👤 Assigned to agent: {saved['assigned_to']}")

    print("\n✅ Pipeline test complete!\n")

asyncio.run(test_full_pipeline())