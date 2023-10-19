from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import json
from model import chat
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema.messages import SystemMessage, BaseMessage, messages_from_dict, messages_to_dict
from config import settings


class LangChainAgent:
    def __init__(self,
        system_message: str | None = None,
        initial_message: str | None = None,
        conversation_history: str | None = None) -> None:
        memory = ConversationBufferMemory()
        if system_message is not None:
            memory.chat_memory.add_message(SystemMessage(content=system_message))
        if initial_message is not None:
            memory.chat_memory.add_ai_message(message=initial_message)
        if conversation_history is not None:
            retrieved_messages = messages_from_dict(json.loads(conversation_history))
            retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)
            memory = ConversationBufferMemory(chat_memory=retrieved_chat_history)

        model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", openai_api_key=settings.OPENAI_API_KEY)
        self._chain = ConversationChain(
            llm=model,
            memory=memory,
        )

    def generate_response(self, text) -> str:
        return self._chain.predict(input=text)

    def extract_chat_history_str(self) -> str:
        extracted_messages = self._chain.memory.chat_memory.messages
        ingest_to_db = messages_to_dict(extracted_messages)
        return json.dumps(ingest_to_db)

    def _dict_to_message(self, message: BaseMessage) -> chat.Message:
        return chat.Message(role=message.type, content=message.content)

    def extract_chat_history_chat_history(self) -> chat.ChatHistory:
        extracted_messages = self._chain.memory.chat_memory.messages
        return chat.ChatHistory(messages=[self._dict_to_message(m) for m in extracted_messages])
