import os

from fastapi import APIRouter, HTTPException, Depends
from fastapi.openapi.models import Response
from fastapi.responses import FileResponse
import logging

from config import settings
from model import service, database_model, chat
from database import table_business, table_survey, table_survey_record, table_template
from fastapi_cognito import CognitoToken
from datetime import datetime
from agent import prompt_templates
from uuid import uuid4

from model.database_model import SurveyRecord
from services.auth import Auth
from services.survey import SurveyService
from services.survey_record import SurveyRecordService, convo_manager
from security import cognito_config

from openpyxl import Workbook

business_table = table_business.BusinessTable()
business_survey_table = table_survey.BusinessSurveyTable()
survey_record_table = table_survey_record.SurveyRecordTable()
template_table = table_template.TemplateTable()

logger = logging.getLogger(__name__)
router = APIRouter()
temp_folder = 'temp'

####### Business related API #######
@router.post("/business/", response_model=service.CreateBusinessResponse)
async def create_business(request: service.CreateBusinessRequest,
                          auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    business_entry = database_model.Business(
        business_name=request.business_name,
        business_description=request.business_description,
        user_id=[auth.username],
        created_at=datetime.utcnow().isoformat(),
    )
    business_table.create_item(business_entry)
    return service.CreateBusinessResponse(**business_entry.model_dump())


@router.put("/business/", response_model=service.UpdateBusinessResponse)
async def update_business(request: service.UpdateBusinessRequest,
                          auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    business = business_table.get_item(request.business_id)
    Auth.validate_permission(business, auth)
    business_entry = database_model.Business(
        business_id=request.business_id,
        business_name=request.business_name,
        business_description=request.business_description,
        user_id=[auth.username],
        created_at=datetime.utcnow().isoformat(),
    )
    ret = business_table.update_business(business_entry)
    return service.UpdateBusinessResponse(**ret)


@router.get("/business", response_model=service.GetBusinessListResponse)
async def get_businesses(auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    businesses = business_table.get_businesses(auth.username)
    return service.GetBusinessListResponse(
        businesses=[service.GetBusinessResponse(**business.model_dump()) for business in businesses])


@router.get("/business/{business_id}", response_model=service.GetBusinessResponse)
async def get_business(business_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    business = business_table.get_item(business_id)
    Auth.validate_permission(business, auth)
    return service.GetBusinessResponse(**business.model_dump())


@router.delete("/business/{business_id}", response_model=Response, operation_id="delete_business")
async def delete_business(business_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    business = business_table.get_item(business_id)
    Auth.validate_permission(business, auth)
    business_table.delete_item(business_id)
    return Response(status_code=204, description="")


####### Survey Related API #######
@router.post("/survey/", response_model=service.CreateSurveyResponse)
async def create_survey(request: service.CreateSurveyRequest,
                        auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    if request.business_id is None:
        business = database_model.Business(
            business_name=request.business_name,
            business_description=request.business_description,
            user_id=[auth.username],
            created_at=datetime.utcnow().isoformat(),
        )
        business_table.create_item(business)
    else:
        business = business_table.get_item(request.business_id)
    Auth.validate_permission(business, auth)
    system_prompt = prompt_templates.system_message_template.format(
        business_name=business.business_name,
        business_description=business.business_description,
        survey_description=request.survey_description,
    )
    initial_message = SurveyService.create_init_message(system_prompt)
    survey_entry = database_model.BusinessSurvey(
        user_id=[auth.username],
        business_id=business.business_id,
        survey_name=request.survey_name,
        survey_description=request.survey_description,
        system_prompt=system_prompt,
        quota=request.quota,
        created_at=datetime.utcnow().isoformat(),
        initial_message=initial_message,
    )
    business_survey_table.create_item(survey_entry)
    response = service.CreateSurveyResponse(**survey_entry.model_dump())

    # add template by id
    template_table.create_item(database_model.Template(
        survey_id=response.survey_id,
    ))

    #     business_info = business_table.get_item(request.business_id)
    #
    #     # TODO: getting initial message relies on the survey_id,
    #     #  make sure initial message does not collide with the default template creation
    #     if request.initial_message is not None:
    #         initial_message = request.initial_message
    #     else:
    #         initial_message = PromptTemplate.from_template(prompt_templates.AGENT_INITIAL_MESSAGE).format(
    #             agent_name="Coco",
    #             business_name=business_info.business_name,
    #         )
    #
    #     system_prompt = PromptTemplate.from_template(prompt_templates.SYSTEM_MESSAGE).format(
    #         business_name=business_info.business_name,
    #         business_description=business_info.business_description,
    #         survey_description=request.survey_description,
    #     )
    #
    #     survey_entry = database_model.BusinessSurvey(
    #         user_id=["fake"],
    #         business_id=request.business_id,
    #         survey_name=request.survey_name,
    #         survey_description=request.survey_description,
    #         system_prompt='todo placeholder',
    #         quota=request.quota,
    #         created_at=datetime.utcnow().isoformat(),
    #         initial_message='todo placeholder',
    #     )
    #     business_survey_table.create_item(survey_entry)
    #     response = service.CreateSurveyResponse(**survey_entry.model_dump())
    #
    #     # add template by id,
    #     template_table.create_item(database_model.Template(
    #         survey_id=response.survey_id,
    #     ))

    return response


@router.get("/survey", response_model=service.ListSurveysResponse, operation_id="get_surveys")
async def get_surveys(auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    survey_entries = business_survey_table.get_surveys(auth.username)
    surveys = []
    for survey in survey_entries:
        surveys.append(SurveyService.build_survey_response(survey))
    return service.ListSurveysResponse(surveys=surveys)


@router.get("/survey/{survey_id}", response_model=service.GetSurveyResponse)
async def get_survey(survey_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    return SurveyService.get_survey(survey_id, auth)


@router.put("/survey/{survey_id}", response_model=service.UpdateSurveyResponse, operation_id="update_survey")
async def update_survey(survey_id: str,
                        request: service.UpdateSurveyRequest,
                        auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    survey = business_survey_table.get_item(survey_id)
    Auth.validate_permission(survey, auth)
    new_survey = database_model.BusinessSurvey(
        survey_id=survey_id,
        survey_name=request.survey_name,
        business_id=survey.business_id,
        quota=survey.quota,
        user_id=survey.user_id,
        created_at=survey.created_at,
        system_prompt=request.system_prompt,
        survey_description=request.survey_description,
        initial_message=request.initial_message,
    )
    business_survey_table.update_survey(new_survey)
    return service.GetSurveyResponse(**business_survey_table.get_item(survey_id).model_dump())


@router.delete("/survey/{survey_id}", response_model=Response, operation_id="delete_survey")
async def delete_survey(survey_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    survey = business_survey_table.get_item(survey_id)
    Auth.validate_permission(survey, auth)
    business_survey_table.delete_item(survey_id)
    return Response(status_code=204, description="")


@router.get("/survey/{survey_id}/insight", response_model=service.GetSurveyInsightResponse)
async def get_survey_insight(survey_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    survey = business_survey_table.get_item(survey_id)
    Auth.validate_permission(survey, auth)
    return service.GetSurveyInsightResponse(survey_insight=survey.insight)


@router.put("/survey/{survey_id}/insight/new", response_model=service.GetSurveyInsightResponse)
async def init_survey_insight(survey_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    survey = business_survey_table.get_item(survey_id)
    Auth.validate_permission(survey, auth)
    insight = SurveyRecordService.init_insight(survey)
    return service.GetSurveyInsightResponse(survey_insight=insight)


# list_surveys needed 
@router.get("/business/{business_id}/survey", response_model=service.ListSurveysByBusinessResponse)
async def get_surveys_list_by_business_id(business_id: str,
                                          auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    business = business_table.get_item(business_id)
    Auth.validate_permission(business, auth)
    survey_entries = business_survey_table.get_surveys(auth.username, business_id)
    return service.ListSurveysByBusinessResponse(
        surveys=[SurveyService.build_survey_response(survey) for survey in survey_entries]
    )


# GET /survey/{survey_id}/records
# get survey id record. pagination, sort. 
@router.get("/survey/{survey_id}/records", response_model=service.ListSurveyRecordsResponse)
async def list_survey_records(survey_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    survey = business_survey_table.get_item(survey_id)
    Auth.validate_permission(survey, auth)
    survey_records = survey_record_table.list_survey_records(survey_id=survey_id)
    return service.ListSurveyRecordsResponse(records=survey_records)


@router.get("/survey/{survey_id}/report/xlsx", response_class=FileResponse)
# async def list_survey_records(survey_id: str, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
async def get_survey_xlsx(survey_id: str):
    survey = business_survey_table.get_item(survey_id)
    # Auth.validate_permission(survey, auth)
    records = survey_record_table.list_survey_records(survey_id=survey.survey_id)
    for record in records:
        if record.summary is None or record.summary == "":
            SurveyRecordService.init_summary(record)
    records = survey_record_table.list_survey_records(survey_id=survey.survey_id)
    insight = SurveyRecordService.init_insight(survey)

    wb = Workbook()
    ws = wb.active

    ws.append(['Survey Insight:'])
    ws.append([insight])
    ws.append(['Chats:'])

    column_headers = list(SurveyRecord.model_fields.keys())
    ws.append(column_headers)

    # Add rows of data to the worksheet
    for record in records:
        row_data = []
        for field in column_headers:
            value = getattr(record, field)
            # Convert lists to a string or some other placeholder
            if isinstance(value, list):
                if not value:  # If the list is empty
                    row_data.append(None)  # or row_data.append('') if you prefer
                else:
                    row_data.append(', '.join(map(str, value)))  # Join non-empty lists with commas
            else:
                row_data.append(value)
        ws.append(row_data)

    file_path = f"{temp_folder}/report-{survey_id}.xlsx"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    wb.save(file_path)
    file = FileResponse(
        path=file_path,
        filename="survey_report.xlsx",
        headers={
            'Content-Disposition': f'attachment; filename="uxmate_survey_report.xlsx"'
        },
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    return file


####### Record related API #######
@router.post("/survey_record/", response_model=service.GetOrCreateSurveyRecordResponse)
async def get_create_survey_record(request: service.GetOrCreateSurveyRecordRequest):
    survey = business_survey_table.get_item(request.survey_id)
    if business_survey_table.get_item(request.survey_id) is None:
        raise HTTPException(status_code=404, detail=f"{request.survey_id=} not found")
    # If FE provided a record_id
    if request.record_id is not None:
        # check cache first
        
        if request.record_id in convo_manager.cache:
            logger.info("record_id found in cache, retrive from cache")
            return service.GetOrCreateSurveyRecordResponse(
                survey_id=request.survey_id,
                record_id=request.record_id,
                survey_name=survey.survey_name,
                description=survey.survey_description,
                record_state=database_model.SurveyRecordState.IN_PROGRESS,
                chat_history=convo_manager.cache[request.record_id].extract_chat_history_chat_history(),
                assistant_name=survey.assistant_name,
            )
        # check DB 
        # TODO: improve this caching logic
        record_entry = survey_record_table.get_item(request.record_id)
        # first check if that record exist, if not return error
        if record_entry is None:
            raise HTTPException(status_code=404, detail=f"{request.record_id=} not found")
        # If record exist, respond directly
        # TODO: load it into cache first
        logger.info("record_id found in db, retrive from db")
        return service.GetOrCreateSurveyRecordResponse(
            survey_id=record_entry.survey_id,
            record_id=record_entry.record_id,
            survey_name=survey.survey_name,
            record_state=record_entry.record_state,
            description=survey.survey_description,
            chat_history=chat.ChatHistory.from_str(record_entry.chat_history),
            assistant_name=survey.assistant_name,)

    # If FE didn't provide record id, create a brand-new record.
    # This means the beginning of the conversation.
    record_id = uuid4().hex
    agent = convo_manager.get_agent_from_record(record_id=record_id, survey_id=request.survey_id)
    record_entry = database_model.SurveyRecord(
        record_id=record_id,
        survey_id=request.survey_id,
        business_id=survey.business_id,
        created_at=datetime.utcnow().isoformat(),
        chat_history=agent.extract_chat_history_str(),
        record_state=database_model.SurveyRecordState.IN_PROGRESS,
        system_message=survey.system_prompt,
    )
    survey_record_table.create_item(record_entry)
    chat_history_messages: chat.ChatHistory = agent.extract_chat_history_chat_history()
    return service.GetOrCreateSurveyRecordResponse(
        survey_id=record_entry.survey_id,
        record_id=record_entry.record_id,
        survey_name=survey.survey_name,
        record_state=record_entry.record_state,
        description=survey.survey_description,
        chat_history=chat_history_messages,
        assistant_name=survey.assistant_name,
    )


@router.get("/survey_record/{record_id}", response_model=service.GetSurveyRecordResponse)
async def get_survey_record(record_id: str):
    record_entry = survey_record_table.get_item(record_id)
    logger.info(f'looking for {record_id=}')
    if record_entry is None:
        raise HTTPException(status_code=404, detail=f"{record_id=} not found")
    return service.GetSurveyRecordResponse(
        survey_id=record_entry.survey_id,
        record_id=record_entry.record_id,
        chat_history=chat.ChatHistory.from_str(record_entry.chat_history),
        record_state=record_entry.record_state,
    )


@router.delete("/survey_record/{record_id}", response_model=Response, operation_id="delete_survey_record")
async def delete_survey_record(record_id: str):
    record_entry = survey_record_table.get_item(record_id)
    if record_entry is None:
        raise HTTPException(status_code=404, detail=f"{record_id=} not found")
    else:
        survey_record_table.delete_item(record_id)
        return Response(status_code=204, description="")


@router.get("/survey_record/{record_id}/summary", response_model=service.GetSurveyRecordSummaryResponse)
async def get_survey_summary(record_id: str):
    record = survey_record_table.get_item(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"{record_id=} not found")
    summary = record.summary if record.summary is not None else "No summary yet. The dialog must be completed."
    return service.GetSurveyRecordSummaryResponse(record_id=record_id, chat_summary=summary)


@router.put("/survey_record/{record_id}/summary/new", response_model=service.GetSurveyRecordSummaryResponse)
async def init_survey_summary(record_id: str):
    record = survey_record_table.get_item(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"{record_id=} not found")
    summary = SurveyRecordService.init_summary(record)
    return service.GetSurveyRecordSummaryResponse(record_id=record_id, chat_summary=summary)


@router.get("/chat_history/{record_id}", response_model=service.GetChatHistoryResponse)
async def get_chat_history(record_id: str):
    # check cache first
    if record_id in convo_manager.cache:
        return service.GetChatHistoryResponse(
            chat_history=convo_manager.cache[record_id].extract_chat_history_chat_history()
        )
    # if not exist, check DB
    record_entry = survey_record_table.get_item(record_id)
    if record_entry is None:
        raise HTTPException(status_code=404, detail=f"{record_id=} not found")
    return service.GetChatHistoryResponse(chat_history=chat.ChatHistory.from_str(record_entry.chat_history))


# post /chat/  chat response
@router.post("/chat/", response_model=service.SendNewMessageResponse)
async def chat_with_bot(request: service.SendNewMessageRequest):
    record = survey_record_table.get_item(request.record_id)
    if record.record_state == database_model.SurveyRecordState.COMPLETED:
        raise HTTPException(status_code=400, detail="This survey has been completed.")

    try:
        history = SurveyRecordService.answer(record, request.message.content)
        if SurveyRecordService.is_completion_goal_reached(history):
            record = SurveyRecordService.complete(record)
        return service.SendNewMessageResponse(messages=history, record_state=record.record_state)
    except Exception as e:
        logger.exception("error found %s, type %s", e, type(e))
        SurveyRecordService.set_state(record, database_model.SurveyRecordState.ERROR)
        raise e

@router.post("/business_and_survey/",
             response_model=service.CreateBusinessAndSurveyResponse)
async def create_business_and_survey(request: service.CreateBusinessAndSurveyRequest, auth: CognitoToken = Depends(cognito_config.cognito_us.auth_required)):
    business_entry = database_model.Business(
        business_name=request.business_name,
        business_description=request.business_description,
        user_id=[auth.username],
        created_at=datetime.utcnow().isoformat(),
    )
    business_table.create_item(business_entry)
    survey_entry = database_model.BusinessSurvey(
        user_id=[auth.username],
        business_id=business_entry.business_id,
        survey_name=request.survey_name,
        survey_description=request.survey_description,
        system_prompt=request.system_prompt,
        quota=request.quota,
        created_at=datetime.utcnow().isoformat(),
        initial_message=request.initial_message,
    )
    business_survey_table.create_item(survey_entry)
    response = service.CreateBusinessAndSurveyResponse(
        business_id=business_entry.business_id,
        survey_id=survey_entry.survey_id,
        chat_link=f"{settings.customer_chat_root_link}/survey/{survey_entry.survey_id}"
    )
    prompt_template = database_model.Template(
        survey_id=response.survey_id,
    )
    template_table.create_item(prompt_template)
    return response
