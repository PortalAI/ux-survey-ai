from fastapi import APIRouter, HTTPException
from .models import Business, BusinessSurvey, CreateBusinessSurveyRequest, CreateBusinessSurveyResponse, SurveySession, UpdateSurveySessionRequest
from .table_ops import BusinessTable, BusinessSurveyTable, SurveySessionTable
from agent import langchain_agent
from boto3.dynamodb.conditions import Key, Attr
from constant import LLM_PREAMBLE
from starlette.requests import Request
import constant
import uuid
from datetime import datetime

router = APIRouter()

business_table = BusinessTable()
business_survey_table = BusinessSurveyTable()
survey_session_table =SurveySessionTable()



@router.post("/create_business_survey/", response_model=CreateBusinessSurveyResponse)
def create_business_survey_endpoint(item: CreateBusinessSurveyRequest):
    business_id = str(uuid.uuid4())
    survey_id = str(uuid.uuid4())
    presentation_link_id = str(uuid.uuid4())
    presentation_password = str(uuid.uuid4())
    business_entry = Business(
        business_id=business_id,
        business_name=item.business_name,
        business_description=item.business_description
    )
    business_survey_entry = BusinessSurvey(
        business_id = business_entry.business_id,
        survey_id = survey_id,
        survey_name = item.survey_name,
        survey_description=item.survey_description,
        chat_prompts = LLM_PREAMBLE.format(
          business_name=item.business_name,
          business_description=item.business_description,
          survey_description=item.survey_description
        ),
        survey_link = f'/chat/{survey_id}',
        presentation_link = f'/presentation/{presentation_link_id}',
        presentation_password = f'{presentation_password}',
        created_at = datetime.utcnow().isoformat(),

    )
    business_table.create_item(business_entry)
    business_survey_table.create_item(business_survey_entry)
    return CreateBusinessSurveyResponse(
        business_id=business_entry.business_id,
        business_name=business_entry.business_name,
        business_description=business_entry.business_description,
        survey_link=f'/chat/{survey_id}',
        presentation_link=business_survey_entry.presentation_link,
        presentation_password=presentation_password,
    )

@router.post("/create_survey_session/{survey_id}")
def create_survey_session(request: Request, survey_id: str):

    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())
    survey_session_table.initiate_survey_session(survey_id=survey_id, session_id=request.session["session_id"])

@router.post("/update_survey_session/")
def update_survey_session(request: Request, update_request: UpdateSurveySessionRequest):
    session_id = request.session.get("session_id") or '793baa9a-20a8-4a34-9c31-282eefde4d9b'
    # survey_id = 'c33c6456-c7b0-4883-b82a-1163173b6240'
    survey_session_table.update_survey_session(
        session_id=session_id,
        **update_request
    )

@router.get("/survey/{survey_id}")
def find_survey_link_id(survey_id: str):
    items = business_survey_table.scan(Attr('survey_id').eq(survey_id))
    if items:
        return
    else:
        raise HTTPException(status_code=404, detail=f"survey id {survey_id} not found")
    

@router.get("/presentation/{presentation_link_id}")
def find_presentation_link_id(presentation_link_id: str):
    items = business_survey_table.scan(Attr('presentation_link').eq(f'/presentation/{presentation_link_id}'))
    if items:
        return
    else:
        raise HTTPException(status_code=404, detail=f"presentation link id {presentation_link_id} not found")
    

@router.get("/business/{business_name}")
def get_business_endpoint(business_name: str):
    return business_table.get_by_business_name(business_name)

@router.get("/business_survey/{survey_name}")
def get_business_survey_endpoint(survey_name: str):
    return business_survey_table.get_by_survey_name(survey_name)


@router.get("/summarize_survey/{presentation_link_id}")
def summarize_survey(presentation_link_id: str):
    items = business_survey_table.scan(Attr('presentation_link').eq(f'/presentation/{presentation_link_id}'))
    if not items:
        raise HTTPException(status_code=404, detail=f"presentation link id {presentation_link_id} not found")
    survey_id = items[0]['survey_id']
    # TODO: summarize the summary field or structure summary field
    surveys = survey_session_table.query(
        Key('survey_id').eq(survey_id))
    summarizations = [survey['summary'] for survey in surveys]
    agent = langchain_agent.LangChainAgent()
    response = agent.generate_response(constant.GENERATE_INSIGHT_PROMPT.format(content='\n'.join(summarizations)))
    return response
