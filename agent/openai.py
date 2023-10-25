import openai

from config import settings

openai.api_key = settings.OPENAI_API_KEY


# TODO: add retries
def complete(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']
