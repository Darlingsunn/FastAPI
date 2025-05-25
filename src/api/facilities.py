from fastapi import Query, Body, APIRouter
from src.api.dependences import DBDep
from src.schemas.facilities import FacilitiesTitle

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def create_facility(
        db: DBDep,
        title: FacilitiesTitle = Body()
):
    facility=await db.facilities.add(title)
    await db.commit()
    return {"status": "OK", "data": facility}