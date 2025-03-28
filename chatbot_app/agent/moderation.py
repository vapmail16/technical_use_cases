from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def moderate_input(user_input):
    response = client.moderations.create(input=user_input)
    result = response.results[0]

    if result.flagged:
        return False, result.categories

    return True, None
