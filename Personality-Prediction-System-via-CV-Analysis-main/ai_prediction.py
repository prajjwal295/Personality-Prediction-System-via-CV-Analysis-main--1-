import google.generativeai as genai
from prediction import personality_traits

genai.configure(api_key="AIzaSyCQddEzfQidcNdtuDbq8SSlO6K3Ds-ayOc")
# proceed here for api key  https://makersuite.google.com/app/apikey

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name= "gemini-1.5-flash",
    generation_config=generation_config,
)

import json

def chat(query):
    for _ in range(3):  # Retry up to 3 times
        try:
            response = model.generate_content([query])
            return response.text  # Assuming the response is in plain text
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
    return "Sorry, I'm unable to assist at the moment."


def say(text):
    print(f"Luna: {text}")

def takeCommand():
    try:
        personality_traits = {
            "o": 2,
            "c": 2,
            "e": 1,
            "a": 0,
            "n": 5
        }
        query = "Describe a candidate's personality based on these traits: " + ', '.join(f"{k}: {v}" for k, v in personality_traits.items())
        return query
    except Exception as e:
        return "Some Error Occurred. Sorry from Luna"

if __name__ == '_main_':
    query = takeCommand()
    response = chat(query)
    json_output = json.loads(response)
    print(f"Luna: {json_output}")