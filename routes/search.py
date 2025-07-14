from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def search_root():
    """Search root endpoint"""
    return {"message": "Hello World", "route": "search"}


@router.get("/health")
async def search_health():
    """Search health check"""
    return {"status": "healthy", "route": "search"}
