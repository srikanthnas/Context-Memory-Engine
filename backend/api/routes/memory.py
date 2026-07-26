from fastapi import APIRouter

router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


@router.get("/")
def memory_status():
    return {
        "message": "Memory Engine endpoint is working"
    }