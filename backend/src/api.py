import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from core.config import CONFIG

from fashion.clothes import router as clothes_router

app = FastAPI(
    title="NextIn API", version="1.0.0", default_response_class=ORJSONResponse
)
app.include_router(clothes_router)


@app.get("/")
async def root():
    return {"message": "Welcome to RFP Lite API"}


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=CONFIG.UVICORN.PORT,
        workers=CONFIG.UVICORN.WORKERS,
        reload=CONFIG.UVICORN.RELOAD_ON_CHANGE,
    )
