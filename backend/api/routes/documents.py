from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("/")
def get_documents():
    return {
        "message": "Documents endpoint is working"
    }