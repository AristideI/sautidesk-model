from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def model_root():
    """Model root endpoint"""
    return {"message": "Hello World", "route": "model"}


@router.get("/predict")
async def model_predict():
    """Model predict endpoint"""
    return {"message": "Hello World", "route": "model", "endpoint": "predict"}


@router.get("/health")
async def model_health():
    """Model health check"""
    return {"status": "healthy", "route": "model"}
