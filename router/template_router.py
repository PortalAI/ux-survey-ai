from fastapi import APIRouter, HTTPException
from model import service, database_model

from database import table_template

template_table = table_template.TemplateTable()

router = APIRouter()


@router.post("/template/", response_model=service.CreateTemplateResponse)
async def create_template(request: service.CreateTemplateRequest):
    # todo see why setting default to None doesn't work
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
    template_entry = database_model.Template(
        template_id=request.template_id,
        survey_id=request.survey_id,
        system_message=request.system_message,
        system_message_params=request.system_message_params,
        agent_initial_message=request.agent_initial_message,
        agent_initial_message_params=request.agent_initial_message_params,
        summary_single_prompt=request.summary_single_prompt,
        summary_single_prompt_params=request.summary_single_prompt_params,
        get_insight_prompt=request.get_insight_prompt,
        get_insight_prompt_params=request.get_insight_prompt_params,
    )
    ret = template_table.update_template(template_entry)
    return service.UpdateTemplateResponse(**ret)


@router.get("/template/{template_id}", response_model=service.GetTemplateResponse)
async def get_template(template_id: str):
    ret = template_table.get_item(template_id)
    if ret is None:
        raise HTTPException(status_code=404, detail=f"{template_id=} not found")

    return service.GetTemplateResponse(**ret.model_dump())
