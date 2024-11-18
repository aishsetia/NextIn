import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import CONFIG
from fashion import router as clothes_router
from fashiongpt import router as fashiongpt_router

app = FastAPI(
    title="NextIn API", version="1.0.0", default_response_class=ORJSONResponse
)
app.include_router(clothes_router)
app.include_router(fashiongpt_router)


@app.get("/")
async def root():
    return {"message": "Welcome to NextIn API"}


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=CONFIG.UVICORN.PORT,
        workers=CONFIG.UVICORN.WORKERS,
        reload=CONFIG.UVICORN.RELOAD_ON_CHANGE,
    )
