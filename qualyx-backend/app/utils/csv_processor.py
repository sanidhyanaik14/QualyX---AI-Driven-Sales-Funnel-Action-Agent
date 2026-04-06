	
'''
# app/utils/csv_processor.py
import pandas as pd
from io import StringIO
from app.services.ai_service import extract_lead, qualify_lead

COLUMN_MAP = {
    'Name': 'name', 'Full Name': 'name',
    'Email': 'email', 'Email Address': 'email',
    'Phone': 'phone', 'Mobile': 'phone',
    'Company': 'company', 'Organisation': 'company',
    'Interest': 'interest', 'Product': 'interest',
    'Budget': 'budget', 'Message': 'message_raw',
}

async def process_csv(file_bytes: bytes) -> list[dict]:
    
    content = file_bytes.decode('utf-8', errors='replace')
    df = pd.read_csv(StringIO(content))

    # Normalise column names
    df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns},
              inplace=True)
    df.fillna('', inplace=True)

    results = []
    for _, row in df.iterrows():
        lead = row.to_dict()

        # If 'message_raw' present but no structured fields → AI extract
        if lead.get('message_raw') and not lead.get('interest'):
            try:
                extracted = await extract_lead(lead['message_raw'])
                lead.update({k: v for k, v in extracted.items() if v})
            except Exception:
                pass

        # AI qualification
        try:
            qual = await qualify_lead(lead)
            lead['score']         = qual['score']
            lead['qualification'] = qual['qualification']
            lead['ai_reasoning']  = qual.get('reasoning', '')
        except Exception:
            lead['score'] = 0
            lead['qualification'] = 'cold'

        lead['source'] = 'csv_upload'
        results.append(lead)

    return results
'''
# app/utils/csv_processor.py
import pandas as pd
from io import StringIO
from app.services.ai_service import qualify_lead

COLUMN_MAP = {
    'Name': 'name', 'Full Name': 'name',
    'Email': 'email', 'Email Address': 'email',
    'Phone': 'phone', 'Mobile': 'phone',
    'Company': 'company', 'Organisation': 'company',
    'Interest': 'interest', 'Product': 'interest',
    'Budget': 'budget', 'Message': 'message_raw',
    'Urgency': 'urgency',
}

VALID_URGENCY = {'high', 'medium', 'low'}

def clean_value(val) -> str:
    """Convert any value to clean string, remove .0 from numbers."""
    if val is None or val == '':
        return ''
    s = str(val).strip()
    # Convert "9876543210.0" → "9876543210"
    if s.endswith('.0') and s[:-2].isdigit():
        s = s[:-2]
    return s

async def process_csv(file_bytes: bytes) -> list[dict]:
    content = file_bytes.decode('utf-8', errors='replace')
    
    # Read all columns as string to avoid float conversion
    df = pd.read_csv(StringIO(content), dtype=str)

    # Normalize column names
    df.rename(columns={k: v for k, v in COLUMN_MAP.items() if k in df.columns}, inplace=True)
    df = df.where(pd.notnull(df), '')

    results = []
    for _, row in df.iterrows():
        lead = {}
        for k, v in row.to_dict().items():
            cleaned = clean_value(v)
            if cleaned:
                lead[k] = cleaned

        # Validate urgency — must be high/medium/low
        urgency = lead.get('urgency', '').lower().strip()
        lead['urgency'] = urgency if urgency in VALID_URGENCY else 'low'

        # Skip rows with no name
        if not lead.get('name'):
            continue

        # AI qualification
        try:
            qual = await qualify_lead(lead)
            lead['score'] = qual['score']
            lead['qualification'] = qual['qualification']
            lead['ai_reasoning'] = qual.get('reasoning', '')
        except Exception as e:
            print(f"AI error for {lead.get('name')}: {e}")
            lead['score'] = 0
            lead['qualification'] = 'cold'
            lead['ai_reasoning'] = ''

        lead['source'] = 'csv_upload'
        results.append(lead)

    return results