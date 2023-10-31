import logging
import log_config
import uvicorn
from fastapi import FastAPI, Depends, Request
import uuid
from router import basic_router, template_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi_cognito import CognitoToken
from config import settings
from security import cognito_config


log_config.setup_logging()
logger = logging.getLogger(__name__)
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
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    log_config.request_id_var.set(str(uuid.uuid4()))
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    logger.info("hello")
    return {"message": "Hello World", "version": "0.3.3", "version_detail": "increase chats to 60"}


@app.get("/health_check")
async def health_check():
    return {"message": "server is healthy"}


app.include_router(basic_router.router)
app.include_router(template_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
