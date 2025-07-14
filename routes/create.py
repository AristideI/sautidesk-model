from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def create_root():
    """Create root endpoint"""
    return {"message": "Hello World", "route": "create"}


@router.get("/health")
async def create_health():
    """Create health check"""
    return {"status": "healthy", "route": "create"}
