# app/services/lead_service.py (assignment section)
"""
import asyncpg
from app.database import get_db

async def get_best_agent(score: int) -> dict | None:
    '''Assign by highest close_rate for hot/warm; random for cold.'''
    db = await get_db()
    if score >= 40:  # hot or warm
        row = await db.fetchrow('''
            SELECT id, name, close_rate FROM agents
            WHERE is_active = TRUE
            ORDER BY close_rate DESC
            LIMIT 1
        ''')
    else:  # cold
        row = await db.fetchrow('''
            SELECT id, name FROM agents
            WHERE is_active = TRUE
            ORDER BY RANDOM() LIMIT 1
        ''')
    return dict(row) if row else None

async def create_lead(data: dict) -> dict:
    agent = await get_best_agent(data.get('score', 0))
    data['assigned_to'] = agent['id'] if agent else None
    db = await get_db()
    row = await db.fetchrow('''
        INSERT INTO leads (name, email, phone, company, interest,
          budget, urgency, score, qualification, source, assigned_to,
          notes, ai_reasoning, message_raw)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
        RETURNING *
    ''', data['name'], data.get('email'), data.get('phone'),
        data.get('company'), data.get('interest'), data.get('budget'),
        data.get('urgency','low'), data.get('score',0),
        data.get('qualification','cold'), data.get('source','csv_upload'),
        data.get('assigned_to'), data.get('notes'),
        data.get('ai_reasoning'), data.get('message_raw'))
    lead = dict(row)
    await _log_activity(lead['id'], 'lead_created',
        f'Lead created from {data["source"]}')
    if agent:
        await _log_activity(lead['id'], 'assigned',
            f'Assigned to {agent["name"]} (score-based)')
    return lead
"""

"""
from app.database import get_db

async def get_best_agent(score: int):
    db = await get_db()
    try:
        if score >= 40:
            row = await db.fetchrow('''
                SELECT id, name FROM agents
                WHERE is_active = TRUE
                ORDER BY close_rate DESC LIMIT 1
            ''')
        else:
            row = await db.fetchrow('''
                SELECT id, name FROM agents
                WHERE is_active = TRUE
                ORDER BY RANDOM() LIMIT 1
            ''')
        return dict(row) if row else None
    finally:
        await db.close()

async def create_lead(data: dict) -> dict:
    agent = await get_best_agent(data.get('score', 0))
    data['assigned_to'] = str(agent['id']) if agent else None

    db = await get_db()
    try:
        row = await db.fetchrow('''
            INSERT INTO leads (name, email, phone, company, interest,
            budget, urgency, score, qualification, source, assigned_to,
            notes, ai_reasoning, message_raw)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
            RETURNING *
        ''',
        data.get('name', 'Unknown'),
        data.get('email'),
        data.get('phone'),
        data.get('company'),
        data.get('interest'),
        data.get('budget'),
        data.get('urgency', 'low'),
        int(data.get('score', 0)),
        data.get('qualification', 'cold'),
        data.get('source', 'csv_upload'),
        data.get('assigned_to'),
        data.get('notes'),
        data.get('ai_reasoning'),
        data.get('message_raw'))

        return dict(row)
    finally:
        await db.close()

async def bulk_create_leads(leads: list) -> dict:
    results = {'hot': 0, 'warm': 0, 'cold': 0, 'errors': 0}
    for lead in leads:
        try:
            saved = await create_lead(lead)
            q = saved.get('qualification', 'cold')
            results[q] = results.get(q, 0) + 1
        except Exception as e:
            print(f"Error saving lead: {e}")
            results['errors'] += 1
    return results

"""

from app.database import get_db
from app.auth import get_current_user

async def create_lead(data: dict, user_id: str) -> dict:
    agent = await get_best_agent(data.get('score', 0), user_id)
    data['assigned_to'] = str(agent['id']) if agent else None

    db = await get_db()
    try:
        row = await db.fetchrow('''
            INSERT INTO leads (name, email, phone, company, interest,
            budget, urgency, score, qualification, source, assigned_to,
            notes, ai_reasoning, message_raw, user_id)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)
            RETURNING *
        ''',
        data.get('name', 'Unknown'),
        data.get('email'),
        data.get('phone'),
        data.get('company'),
        data.get('interest'),
        data.get('budget'),
        data.get('urgency', 'low'),
        int(data.get('score', 0)),
        data.get('qualification', 'cold'),
        data.get('source', 'csv_upload'),
        data.get('assigned_to'),
        data.get('notes'),
        data.get('ai_reasoning'),
        data.get('message_raw'),
        user_id)
        return dict(row)
    finally:
        await db.close()

async def get_best_agent(score: int, user_id: str):
    db = await get_db()
    try:
        if score >= 40:
            row = await db.fetchrow('''
                SELECT id, name FROM agents
                WHERE is_active = TRUE AND user_id = $1
                ORDER BY close_rate DESC LIMIT 1
            ''', user_id)
        else:
            row = await db.fetchrow('''
                SELECT id, name FROM agents
                WHERE is_active = TRUE AND user_id = $1
                ORDER BY RANDOM() LIMIT 1
            ''', user_id)
        return dict(row) if row else None
    finally:
        await db.close()

async def bulk_create_leads(leads: list, user_id: str) -> dict:
    results = {'hot': 0, 'warm': 0, 'cold': 0, 'errors': 0}
    for lead in leads:
        try:
            saved = await create_lead(lead, user_id)
            q = saved.get('qualification', 'cold')
            results[q] = results.get(q, 0) + 1
        except Exception as e:
            print(f"Error saving lead: {e}")
            results['errors'] += 1
    return results

async def get_leads(user_id: str) -> list:
    db = await get_db()
    try:
        rows = await db.fetch('''
            SELECT * FROM leads
            WHERE user_id = $1
            ORDER BY created_at DESC
        ''', user_id)
        return [dict(r) for r in rows]
    finally:
        await db.close()

async def get_stats(user_id: str) -> dict:
    db = await get_db()
    try:
        row = await db.fetchrow('''
            SELECT
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE qualification = 'hot') as hot,
                COUNT(*) FILTER (WHERE qualification = 'warm') as warm,
                COUNT(*) FILTER (WHERE qualification = 'cold') as cold
            FROM leads WHERE user_id = $1
        ''', user_id)
        return dict(row)
    finally:
        await db.close()