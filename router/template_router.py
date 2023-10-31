from fastapi import APIRouter, HTTPException
from model import service, database_model

from database import table_template, table_survey

template_table = table_template.TemplateTable()
business_survey_table = table_survey.BusinessSurveyTable()

router = APIRouter()


@router.post("/template/", response_model=service.CreateTemplateResponse)
async def create_template(request: service.CreateTemplateRequest):

    # TODO see why setting default to None doesn't work
    # TODO add check logic (whether survey id is in the index)

    template_entry = database_model.Template(
        survey_id=request.survey_id,
        # system_message=request.system_message,
        # system_message_params=request.system_message_params,
        # agent_initial_message=request.agent_initial_message,
        # agent_initial_message_params=request.agent_initial_message_params,
        # summary_single_prompt=request.summary_single_prompt,
        # summary_single_prompt_params=request.summary_single_prompt_params,
        # get_insight_prompt=request.get_insight_prompt,
        # get_insight_prompt_params=request.get_insight_prompt_params,
    )
    template_table.create_item(template_entry)
    return service.CreateTemplateResponse(**template_entry.model_dump())


@router.put("/template/", response_model=service.UpdateTemplateResponse)
async def update_template(request: service.UpdateTemplateRequest):
    if not business_survey_table.survey_exist(request.survey_id):
        raise HTTPException(status_code=404, detail=f"{request.survey_id=} not found")
    business_survey_table.update_prompts()
    return None



@router.get("/template/{template_id}", response_model=service.GetTemplateResponse)
async def get_template(template_id: str):
    ret = template_table.get_item(template_id)
    if ret is None:
        raise HTTPException(status_code=404, detail=f"{template_id=} not found")

    return service.GetTemplateResponse(**ret.model_dump())


@router.get("/survey/{survey_id}/template", response_model=service.GetTemplateResponse)
async def get_template_by_survey_id(survey_id: str):
    template = template_table.get_by_survey_id(survey_id)
    if template is None or not template:
        raise HTTPException(status_code=404, detail=f"{survey_id=} not found")
    return service.GetTemplateResponse(**template.model_dump())
