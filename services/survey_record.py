from conversation.factory import ConversationImplementation, build_conversation_manager
from conversation.open_ai import complete
from database import table_survey_record, table_survey
from model.chat import ChatHistory
from model.database_model import SurveyRecord, SurveyRecordState, BusinessSurvey
from router.template_router import template_table
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)
survey_record_table = table_survey_record.SurveyRecordTable()
business_survey_table = table_survey.BusinessSurveyTable()

conversation_manager = build_conversation_manager(ConversationImplementation.OpenaiAssistant)


class SurveyRecordService:

    @staticmethod
    def answer(record: SurveyRecord, question: str) -> ChatHistory:
        SurveyRecordService.set_state(record, SurveyRecordState.IN_PROGRESS)
        conversation = conversation_manager.get_conversation(record.record_id)
        if conversation is None:
            raise RuntimeError(f"Conversation for record {record.record_id} was not found to reply")
        logger.info("Generating response")
        conversation.reply(question)
        logger.info("Saving the response to the history")
        survey_record_table.update_chat_history(record.record_id, conversation.stringify_chat_history())
        return conversation.extract_chat_history()

    @staticmethod
    def complete(record: SurveyRecord) -> SurveyRecord:
        SurveyRecordService.init_summary(record)
        # survey = business_survey_table.get_item(record.survey_id)
        # SurveyRecordService.init_insight(survey)
        SurveyRecordService.set_state(record, SurveyRecordState.COMPLETED)
        return record

    @staticmethod
    def init_summary(record: SurveyRecord) -> str:
        conversation = conversation_manager.get_conversation(record.record_id)
        if conversation is None:
            raise RuntimeError(f"Conversation for record {record.record_id} was not found to init summary")
        templates = template_table.get_by_survey_id(record.survey_id)
        summary_prompt_template = PromptTemplate.from_template(templates.summary_single_prompt)
        summary_prompt = summary_prompt_template.format(conversation=conversation.stringify_chat_history())
        summary = complete(summary_prompt)
        survey_record_table.update_summary(record.record_id, complete(summary_prompt))
        return summary

    @staticmethod
    def init_insight(survey: BusinessSurvey) -> str:
        templates = template_table.get_by_survey_id(survey.survey_id)
        survey = business_survey_table.get_item(survey.survey_id)
        records = survey_record_table.list_survey_records(survey_id=survey.survey_id)
        summaries = [record.summary for record in records if record.summary != "" and record.summary is not None]
        # TODO: cut prompt to fit into the context
        insight_prompt_template = PromptTemplate.from_template(templates.get_insight_prompt)
        if "{goal}" in insight_prompt_template:
            insight_prompt_template = insight_prompt_template.replace("{goal}", survey.system_prompt)
        insight_prompt = insight_prompt_template.format(summaries='\n'.join(summaries))
        
        insight = complete(insight_prompt)
        business_survey_table.update_survey_insight(survey.survey_id, insight)
        return insight

    @staticmethod
    def set_state(record: SurveyRecord, state: SurveyRecordState):
        record.record_state = state
        survey_record_table.update_record_state(record.record_id, record.record_state)
        return record

    @staticmethod
    def is_completion_goal_reached(chat: ChatHistory) -> bool:
        if "TERMINATE" in chat.messages[-1].content:
            chat.messages[-1].content = chat.messages[-1].content.replace("TERMINATE", "")
            # breakpoint()
            return True
        return len(chat.messages) > 60
