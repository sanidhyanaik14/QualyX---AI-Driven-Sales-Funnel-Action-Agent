from fastapi import APIRouter
router = APIRouter(prefix='/api/webhooks', tags=['webhooks'])

@router.get('/health')
async def health():
    return {'status': 'ok'}