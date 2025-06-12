from fastapi import Body, APIRouter
from src.api.dependences import DBDep
from src.schemas.facilities import FacilitiesTitle

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(
        db: DBDep,
        facility_data: FacilitiesTitle = Body()
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
