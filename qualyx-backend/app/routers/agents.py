from fastapi import APIRouter
router = APIRouter(prefix='/api/agents', tags=['agents'])

@router.get('/')
async def list_agents():
    from app.database import get_db
    db = await get_db()
    try:
        rows = await db.fetch('SELECT * FROM agents')
        return [dict(r) for r in rows]
    finally:
        await db.close()