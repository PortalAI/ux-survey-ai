import logging
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from database.db_routers import router as db_routers
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import constant
from agent import langchain_agent
from database import table_ops

from fastapi.middleware.cors import CORSMiddleware
    

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = FastAPI(docs_url=None)

app.add_middleware(
    SessionMiddleware, secret_key=constant.SESSION_SECRET_KEY, max_age=3600  # 1 hour
)
survey_table = table_ops.SurveySessionTable()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # can alter with time
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# app.mount("/front", StaticFiles(directory="front/public", html=True), name="front")
# app.mount("/build", StaticFiles(directory="front/public/build"), name="build")

@app.get("/")
async def front():
   return RedirectResponse(url='front')

@app.get("/health_check")
async def health_check():
    return {"message": "hello"}

# @app.get("/set/")
# def set_session(request: Request):
#     request.session["foo"] = "bar"
#     return {"status": "session value set"}

# @app.get("/get/")
# def get_session(request: Request):
#     value = request.session.get("foo")
#     return {"session value": value}

# @app.post("/initialize_session")
# def initialize_session(request: Request):
#     pass

@app.websocket("/chat")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    # session_id = request.session.get("session_id")
    # survey_id = request.session.get("survey_id")
    session_id = 'session_id_1'
    survey_id = 'survey_id_1'
    # insert a new entry in survey session
    survey_table.initiate_survey_session(survey_id=survey_id, session_id=session_id)
    try:
        agent = langchain_agent.LangChainAgent()
        while True:
            data = await websocket.receive_text()
            response = agent.generate_response(data)
            await websocket.send_text(f"bot responded: {response}")
    except WebSocketDisconnect:
        # store chat summary into session table
        summary = agent.generate_response(constant.SUMMARIZATION_PROMPT)
        survey_table.update_survey_session(
            session_id=session_id,
            survey_id=survey_id,
            chat_history=agent.memory.buffer,
            summary=summary
        )
        print(f'client #{str(id(websocket))} is disconnected')


app.include_router(db_routers)
