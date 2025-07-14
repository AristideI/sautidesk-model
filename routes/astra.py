from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def astra_root():
    """Astra root endpoint"""
    return {"message": "Hello World", "route": "astra"}


@router.get("/health")
async def astra_health():
    """Astra health check"""
    return {"status": "healthy", "route": "astra"}
