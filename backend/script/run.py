import csv
from agent import langchain_agent
# from prompts import SUMMARY_ALL, SUMMARY_ONE
import prompts
from pydantic import BaseModel
import uuid
from datetime import datetime
from database import table_ops


class SurveySession(BaseModel):
    survey_id: str
    session_id: str
    chat_history: str | None
    summary: str | None
    structured_summary: dict | None
    created_at: str
    updated_at: str

CSV_FILE = '/Users/samhe/projects/portal-ai/hackathon0914UXAI/ux-survey-ai/backend/script/alex_chat.csv'
# legionfarm
SURVEY_ID = 'fb9da499-e155-487f-815c-391bd8477354'

def load_csv_into_list(filename):
    with open(filename, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Convert the CSV reader object into a list of lists
        data = [row for row in csv_reader]
    return data




if __name__ == "__main__":
    data_list = load_csv_into_list(CSV_FILE)
    survey_session_table = table_ops.SurveySessionTable()
    i = 0
    for row in data_list:
        i+=1
        print(i)
        agent = langchain_agent.LangChainAgent()
        chat_history = row[0]
        chat_hist_summary = agent.generate_response(prompts.SUMMARY_ONE.format(data=chat_history))
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        entry = SurveySession(
            survey_id=SURVEY_ID,
            session_id=session_id,
            chat_history=chat_history,
            summary=chat_hist_summary,
            structured_summary=None,
            created_at=now,
            updated_at=now,
        )
        try:
            survey_session_table.create_item(entry)
        except: 
            continue

        

