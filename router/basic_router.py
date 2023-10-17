from fastapi import APIRouter, HTTPException
from model import service, database_model
from database import table_business, table_survey, table_survey_record
from datetime import datetime
from agent import conversation_manager, prompt_templates


business_table = table_business.BusinessTable()
business_survey_table = table_survey.BusinessSurveyTable()
survey_record_table = table_survey_record.SurveyRecordTable()
convo_manager = conversation_manager.ConversationManager(cache_size=100, ttl=100)

router = APIRouter()
####### Business related API #######
@router.post("/business/", response_model=service.CreateBusinessResponse)
async def create_business(request: service.CreateBusinessRequest):
    business_entry = database_model.Business(
        business_name=request.business_name,
        business_description=request.business_description,
        user_id=["fake"],
        created_at=datetime.utcnow().isoformat(),
    )
    business_table.create_item(business_entry)
    return service.CreateBusinessResponse(**business_entry.model_dump())
    
@router.put("/business/", response_model=service.UpdateBusinessResponse)
async def update_business(request: service.UpdateBusinessRequest):
    business_entry = database_model.Business(
        business_id=request.business_id,
        business_name=request.business_name,
        business_description=request.business_description,
        user_id=["fake"]
    )
    ret = business_table.update_business(business_entry)
    return service.UpdateBusinessResponse(**ret)
    
@router.get("/business/{business_id}", response_model=service.GetBusinessResponse)
async def get_business(business_id: str):

    ret = business_table.get_item({'business_id': business_id})
    if ret is None:
        raise HTTPException(status_code=404, detail=f"{business_id=} not found")
    return service.GetBusinessResponse(**ret)
    

####### Survey Related API #######
@router.post("/survey/", response_model=service.CreateSurveyResponse)
async def create_survey(request: service.CreateSurveyRequest):
    business_info = business_table.get_item(request.business_id)
    initial_message = (request.initial_message 
                       if request.initial_message is not None
                       else prompt_templates.agent_initial_message_template.format(
                           agent_name="Coco",
                           business_name=business_info.business_name,
                       ))
    survey_entry = database_model.BusinessSurvey(
        user_id=["fake"],
        business_id=request.business_id,
        survey_name=request.survey_name,
        survey_description=request.survey_description,
        system_prompt=prompt_templates.system_message_template.format(
            business_name=business_info.business_name,
            business_description=business_info.business_description,
            survey_description=request.survey_description,
        ),
        initial_message=initial_message,
    )
    business_survey_table.create_item(survey_entry)
    return service.CreateSurveyResponse(**survey_entry.model_dump())


@router.put("/survey/", response_model=service.UpdateSurveyResponse)
async def update_survey(request: service.UpdateSurveyRequest):
    pass

# get_survey needed
# response insight. (wait until all the)
@router.get("/survey/{survey_id}", response_model=service.GetSurveyResponse)
async def get_survey(survey_id: str):
    pass

# GET /survey/{survey_id}/insight
@router.get("/survey/{survey_id}/insight", response_model=service.GetSurveyInsightResponse)
async def get_survey_insight() :
    pass

# list_surveys needed 
@router.get("/surveys/{business_id}", response_model=service.ListSurveysByBusinessResponse)
async def get_surveys_list_by_business_id(business_id: str):
    pass

# GET /survey/{survey_id}/records
# get survey id record. pagination, sort. 
@router.get("/survey/{survey_id}/records")
async def list_records_by_survey():
    pass

####### Record related API #######

@router.post("/survey_record/", response_model=service.CreateSurveyRecordResponse)
async def create_survey_record(request: service.CreateSurveyRecordRequest):
    # TODO: verify survey and business exist
    record_entry = database_model.SurveyRecord(
        survey_id=request.survey_id,
        business_id=request.business_id,
        created_at=datetime.utcnow().isoformat()
    )
    survey_record_table.create_item(record_entry)
    return service.CreateSurveyRecordResponse(**record_entry.model_dump())
    

@router.get("/chat_history/{record_id}", response_model=service.GetChatHistoryResponse)
async def get_chat_history(record_id: str):
    record_entry = survey_record_table.get_item(record_id)
    return record_entry.get("chat_history")

# post /chat/  chat response 
@router.post("/chat/", response_model=service.SendNewMessageResponse)
async def chat(request: service.SendNewMessageRequest):
    agent = convo_manager.get_agent_from_record(record_id=request.record_id, survey_id=request.survey_id)
    agent.generate_response(request.message)
    return service.SendNewMessageResponse(message=agent.extract_chat_history())


