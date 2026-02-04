from fastapi import APIRouter
router = APIRouter()

@router.get('/athlete/{athlete_id}')
async def get_athlete_statistics(athlete_id: str):
    return {'message': 'Statistics endpoint'}