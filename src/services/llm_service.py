import os

from dotenv import load_dotenv
from openai import OpenAI

#TODO: Aqui crea un system prompt adecuado para el proyecto.
SYSTEM_PROMPT = '''
As an AI assistant, you are tasked with providing helpful and accurate responses to user queries. You should always respond in English, regardless of the language used in the user's message. Your responses should be clear, concise, and informative, while maintaining a friendly and approachable tone.
''' 

def call_llm_with_sdk(user_prompt: str) -> str:
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    )
    return response.choices[0].message.content


def call_llm_with_http(user_prompt: str) -> str:
    pass
