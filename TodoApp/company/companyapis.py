from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_company_name():
    return {"company_name": "company example , LLC"}

@router.get("/employee")
async def numer_of_employee():
    return 265
