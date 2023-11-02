from langchain.prompts import PromptTemplate


# TODO consider turning this logic into a class
SYSTEM_MESSAGE = """
You are CEO's assistant of {business_name}
The business is about {business_description}
You are reaching out to user of the {business_name} and trying to do user research about {survey_description}.
You will follow the moms test and 5 why methodology. Dive deep into conversation with the user and understand what 
are they really looking need deep down.
Reply "TERMINATE" in the end when you think the conversation is done.
"""
# todo should have in the future but for now introducing a change fails the test
# SYSTEM_MESSAGE = """
# You are CEO's assistant of {business_name}. Here is the business description:
# {business_description}
# ####
# You are reaching out to user of the {business_name} and trying to do user research based on the following survey description:
# {survey_description}
# ####
# You will follow the moms test and 5 why methodology. Dive deep into conversation with the user and understand what
# are they really looking need deep down.
# """
SYSTEM_MESSAGE_PARAMS = ['business_name', 'business_description', 'survey_description']
system_message_template = PromptTemplate.from_template(SYSTEM_MESSAGE)

AGENT_INITIAL_MESSAGE = """
Hi I'm {agent_name}, the executive assistant for CEO of {business_name}, I want to personally reach out to ask you some questions about your recent experience if you have time?
"""
AGENT_INITIAL_MESSAGE_PARAMS = ['agent_name', 'business_name']
agent_initial_message_template = PromptTemplate.from_template(AGENT_INITIAL_MESSAGE)

# SUMMARY_SINGLE_PROMPT
SUMMARY_SINGLE_PROMPT = """
Summarize the following conversation. Focus on what human said: 
{conversation}
"""
SUMMARY_SINGLE_PROMPT_PARAMS = ['conversation']

# GET_INSIGHT_PROMPT
GET_INSIGHT_PROMPT = """
The goal of the conversation was:
{goal}
What are the key insights from the following summaries:
{summaries}
"""
GET_INSIGHT_PROMPT_PARAMS = ['goal', 'summaries']
