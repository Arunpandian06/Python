from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def authorized_user():
    return {"message": "This is authorized API"};