from fastapi import APIRouter, HTTPException
from model import service, database_model
from database import table_business, table_survey, table_survey_record



business_table = table_business.BusinessTable()
business_survey_table = table_survey.BusinessSurveyTable()
survey_session_table = table_survey_record.SurveyRecordTable()

router = APIRouter()
# Business related API
@router.post("/create_business/", response_model=service.CreateBusinessResponse)
async def create_business(request: service.CreateBusinessRequest):
    business_entry = database_model.Business(
        business_name=request.business_name,
        business_description=request.business_description,
        user_id=["fake"]
    )
    business_table.create_item(business_entry)
    return service.CreateBusinessResponse(**business_entry.model_dump())
    
@router.put("/update_business/", response_model=service.UpdateBusinessResponse)
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
    return service.GetBusinessResponse(**ret)
    

# Survey Related API
@router.post("/create_survey/", response_model=service.CreateSurveyResponse)
async def create_survey(request: service.CreateSurveyRequest):
    initial_message = request.initial_message if request.initial_message is not None  else "some default mesage"
    survey_entry = database_model.BusinessSurvey(
        user_id=["fake"],
        business_id=request.business_id,
        survey_name=request.survey_name,
        survey_description=request.survey_description,
        system_prompt="System message",
        initial_message=initial_message,
    )
    business_survey_table.create_item(survey_entry)
    return service.CreateSurveyResponse(**survey_entry.model_dump())


@router.put("/update_survey/", response_model=service.UpdateSurveyResponse)
async def update_survey(request: service.UpdateSurveyRequest):
    
    business_survey_table.update_survey()

# get_survey

# list_survey



# # Survey Record API
# create_survey_record

# update_survey_record

# chat_history


