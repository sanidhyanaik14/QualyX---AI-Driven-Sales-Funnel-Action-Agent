'''	
# app/routers/leads.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services import lead_service, email_service, whatsapp_service
from app.services.calendar_service import schedule_meeting
from app.utils.csv_processor import process_csv
from app.models.lead import LeadCreate, LeadUpdate

router = APIRouter(prefix='/api/leads', tags=['leads'])

@router.get('/')                       # List leads with filters
async def list_leads(
    qualification: str | None = None,
    stage: str | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = Query(20, le=100),
):
    return await lead_service.get_leads(
        qualification=qualification, stage=stage,
        search=search, page=page, limit=limit)

@router.get('/stats')                  # Dashboard funnel stats
async def get_stats():
    return await lead_service.get_funnel_stats()

@router.post('/')                      # Create single lead
async def create_lead(data: LeadCreate):
    return await lead_service.create_lead(data.model_dump())

@router.post('/upload-csv')            # Bulk CSV upload
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, 'Only .csv files accepted')
    content = await file.read()
    leads   = await process_csv(content)
    results = await lead_service.bulk_create_leads(leads)
    return {'success': True, 'processed': len(leads), 'results': results}

@router.get('/{lead_id}')              # Single lead
async def get_lead(lead_id: str):
    lead = await lead_service.get_lead_by_id(lead_id)
    if not lead: raise HTTPException(404, 'Lead not found')
    return lead

@router.patch('/{lead_id}')            # Update lead
async def update_lead(lead_id: str, data: LeadUpdate):
    return await lead_service.update_lead(lead_id, data.model_dump(exclude_none=True))

@router.post('/{lead_id}/email')       # Send email
async def send_email(lead_id: str):
    lead = await lead_service.get_lead_by_id(lead_id)
    if not lead: raise HTTPException(404, 'Lead not found')
    return await email_service.send_lead_email(lead)

@router.post('/{lead_id}/whatsapp')    # Send WhatsApp
async def send_whatsapp(lead_id: str):
    lead = await lead_service.get_lead_by_id(lead_id)
    if not lead: raise HTTPException(404, 'Lead not found')
    return await whatsapp_service.send_message(lead)

@router.post('/{lead_id}/schedule')    # Schedule meeting
async def schedule(lead_id: str, body: dict = {}):
    lead = await lead_service.get_lead_by_id(lead_id)
    if not lead: raise HTTPException(404, 'Lead not found')
    return await schedule_meeting(lead, body)

@router.get('/{lead_id}/activity')    # Activity log
async def get_activity(lead_id: str):
    return await lead_service.get_lead_activity(lead_id)'''
"""
# app/routers/leads.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.lead_service import create_lead, bulk_create_leads
from app.utils.csv_processor import process_csv

router = APIRouter(prefix='/api/leads', tags=['leads'])

@router.get('/health')
async def health():
    return {'status': 'ok'}

@router.post('/upload-csv')
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, 'Only .csv files accepted')
    content = await file.read()
    leads = await process_csv(content)
    results = await bulk_create_leads(leads)
    return {
        'success': True,
        'processed': len(leads),
        'results': results
    }

@router.post('/')
async def create_single_lead(data: dict):
    return await create_lead(data)

@router.get('/')
async def list_leads():
    from app.database import get_db
    db = await get_db()
    try:
        rows = await db.fetch('SELECT * FROM leads ORDER BY created_at DESC LIMIT 50')
        return [dict(r) for r in rows]
    finally:
        await db.close()
        """
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.lead_service import create_lead, bulk_create_leads, get_leads, get_stats
from app.utils.csv_processor import process_csv
from app.auth import get_current_user

router = APIRouter(prefix='/api/leads', tags=['leads'])

@router.post('/upload-csv')
async def upload_csv(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, 'Only .csv files accepted')
    content = await file.read()
    leads = await process_csv(content)
    results = await bulk_create_leads(leads, user_id)
    return {'success': True, 'processed': len(leads), 'results': results}

@router.get('/')
async def list_leads(user_id: str = Depends(get_current_user)):
    return await get_leads(user_id)

@router.get('/stats')
async def stats(user_id: str = Depends(get_current_user)):
    return await get_stats(user_id)

@router.post('/')
async def create_single_lead(
    data: dict,
    user_id: str = Depends(get_current_user)
):
    return await create_lead(data, user_id)