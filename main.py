import logging

import uvicorn
from fastapi import FastAPI
from router.basic_router import router as basic_routers
from router.template_router import router as template_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from config import settings

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()

app.add_middleware(
    SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY, max_age=3600  # 1 hour
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World", "version": "0.2.1"}


@app.get("/health_check")
async def health_check():
    return {"message": "server is healthy"}


app.include_router(basic_routers)
app.include_router(template_router)
