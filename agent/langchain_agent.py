import openai
import time
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import json
from model import chat
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema.messages import SystemMessage, BaseMessage, messages_from_dict, messages_to_dict
from config import settings
import logging

logger = logging.getLogger(__name__)
GPT_4 = "gpt-4"
GPT_3_5 = "gpt-3.5-turbo"


class LangChainAgent:
    def __init__(self,
        system_message: str | None = None,
        initial_message: str | None = None,
        conversation_history: str | None = None) -> None:
        memory = ConversationBufferMemory()
        self.gpt_model = GPT_4
        self.falback_start_timer = None
        if system_message is not None:
            memory.chat_memory.add_message(SystemMessage(content=system_message))
        if initial_message is not None:
            memory.chat_memory.add_ai_message(message=initial_message)
        if conversation_history is not None:
            retrieved_messages = messages_from_dict(json.loads(conversation_history))
            retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)
            memory = ConversationBufferMemory(chat_memory=retrieved_chat_history)

        model = ChatOpenAI(temperature=0, model_name=self.gpt_model, openai_api_key=settings.OPENAI_API_KEY, request_timeout=10, max_retries=3)
        self._chain = ConversationChain(
            llm=model,
            memory=memory,
        )
        

    def generate_response(self, text) -> str:
        try:
            if self.gpt_model == GPT_3_5 and self.falback_start_timer is not None and time.time() - self.falback_start_timer > 60:
                self.gpt_model = GPT_4
                self._chain.llm = ChatOpenAI(temperature=0, model_name=self.gpt_model, openai_api_key=settings.OPENAI_API_KEY, request_timeout=10, max_retries=3)            
                logger.info("waited %s before switching to model %s", time.time() - self.falback_start_timer, self._chain.llm.model_name)
                self.falback_start_timer = None
            response = self._chain.predict(input=text)
        except (openai.error.Timeout, openai.error.RateLimitError) as e:
            logger.warning("rate limit hit for model: %s", self.gpt_model)
            if self.gpt_model == GPT_4:
                self.gpt_model = GPT_3_5
                logger.warning("switching to model: %s", self.gpt_model)
                self.falback_start_timer = time.time()
                self._chain.llm = ChatOpenAI(temperature=0, model_name=self.gpt_model, openai_api_key=settings.OPENAI_API_KEY, request_timeout=10, max_retries=3)
                response = self._chain.predict(input=text)
            else:
                logger.exception("model %s throttled", self.gpt_model)
                return None
        except Exception as e:
            logging.error("error found %s, type %s", e, type(e))
        return response

    def extract_chat_history_str(self) -> str:
        extracted_messages = self._chain.memory.chat_memory.messages
        ingest_to_db = messages_to_dict(extracted_messages)
        return json.dumps(ingest_to_db)

    def _dict_to_message(self, message: BaseMessage) -> chat.Message:
        return chat.Message(role=message.type, content=message.content)

    def extract_chat_history_chat_history(self) -> chat.ChatHistory:
        extracted_messages = self._chain.memory.chat_memory.messages
        return chat.ChatHistory(messages=[self._dict_to_message(m) for m in extracted_messages])

    def delete_second_message(self) -> None:
        self._chain.memory.chat_memory.messages.pop(1)
