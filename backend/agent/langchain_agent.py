from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory



class LangChainAgent:
    def __init__(self) -> None:
        self.memory = ConversationBufferMemory()
        model = OpenAI(temperature=0)
        self._chain = ConversationChain(
            llm=model,
            memory=self.memory,
        )

    def generate_response(self, text) -> str:
        return self._chain.predict(input=text)
