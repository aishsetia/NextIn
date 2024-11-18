import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from core.config import CONFIG
from fashion import router as clothes_router
from fashion import uploads_router as clothes_uploads_router
from fashiongpt import router as fashiongpt_router

app = FastAPI(
    title="NextIn API", version="1.0.0", default_response_class=ORJSONResponse
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(clothes_router)
app.include_router(clothes_uploads_router)
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
