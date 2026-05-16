from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.v1.routers import (
    cognitive_model,
    error_prediction,
    adaptive_path,
    growth_tracker,
    affect_detector,
)

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
)

app.include_router(cognitive_model.router, prefix=f"{settings.API_V1}/cognitive-model")
app.include_router(error_prediction.router, prefix=f"{settings.API_V1}/error-prediction")
app.include_router(adaptive_path.router, prefix=f"{settings.API_V1}/adaptive-path")
app.include_router(growth_tracker.router, prefix=f"{settings.API_V1}/growth-tracker")
app.include_router(affect_detector.router, prefix=f"{settings.API_V1}/affect-detector")

@app.get("/")
def root():
    return {"message": "Cognitive Math Twin API is running"}
