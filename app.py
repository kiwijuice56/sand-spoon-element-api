import os
import re
from dotenv import load_dotenv
from flask import Flask, request
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


possible_states = ['liquid', 'gas', 'rigid_solid', 'powdery_solid', 'metal', 'laser', 'electricity', 'creature', 'microbe', 'explosive']


def clean_color(color):
    # Longest valid answer is #FFFFFF
    color = color[:7]

    # Remove erroneous symbols that sometimes appear
    color = '#' + ''.join(c for c in color if c.isalnum())

    # Valid HEX format
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return color
    else:
        return "#FFFFFF"


def clean_state(state):
    # Remove quotes and other punctuation
    state = ''.join(c for c in state if c.isalpha() or c == '_')

    # Strangely, ChatGPT sometimes capitalizes answers
    state = state.lower()

    if state in possible_states:
        return state
    else:
        return 'rigid_solid'


def clean_number(number, default):
    # Sometimes included due to density units
    number = number.replace("-3", "")
    number = ''.join(c for c in number if c.isnumeric() or c == '.')

    try:
        return float(number)
    except:
        return default


def prompt(system_message, user_message):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    return completion.choices[0].message.content, completion.usage.total_tokens


@app.route('/')
def get_custom_element():
    element_name = request.args.get("element_name")[:12]
    if len(element_name) == 0:
        return {}

    moderation_response = client.moderations.create(input=element_name).results[0]
    if moderation_response.flagged:
        return {"warning": "be nice"}


    response = {"element_name": element_name}
    total_tokens = 0

    # General questions for all elements

    answer, prompt_tokens = prompt("Answer in HEX format exactly", f"Color:'{element_name}'")
    response["color_0"] = clean_color(answer)
    total_tokens += prompt_tokens

    answer, prompt_tokens = prompt("Answer in HEX format exactly", f"Color:'{element_name}'")
    response["color_1"] = clean_color(answer)
    total_tokens += prompt_tokens

    answer, prompt_tokens = prompt("Answer only an exact entry from the list:" + "".join(c for c in str(possible_states) if not c == " "),
                                   f"Best description:'{element_name}'")
    response["state"] = clean_state(answer)
    total_tokens += prompt_tokens

    answer, prompt_tokens = prompt("Use no words and always respond in one Kelvin number exactly",
                                   f"Temperature:{element_name}")
    response["temperature"] = max(0, min(10000, clean_number(answer, 298.0)))
    total_tokens += prompt_tokens

    # State-specific questions
    match response["state"]:
        case "liquid":
            answer, prompt_tokens = prompt("Use no words and always respond in one kg*m^-3 number exactly",
                                           f"Density:{element_name}")
            response["density"] = max(0, min(100000, clean_number(answer, 1000.0)))
            total_tokens += prompt_tokens

            answer, prompt_tokens = prompt("Use no words and always respond in one number on a scale from 0.0 to 1.0 exactly",
                                           f"Viscosity:{element_name} (water is 0.8)")
            response["viscosity"] = max(0.0, min(1.0, clean_number(answer, 0.5)))
            total_tokens += prompt_tokens
        case "gas":
            answer, prompt_tokens = prompt("Use no words and always respond in one kg*m^-3 number exactly.",
                                           f"Density:{element_name}")
            response["density"] = max(0, min(100000, clean_number(answer, 1000.0)))
            total_tokens += prompt_tokens
    response["tokens_used"] = total_tokens
    print(response)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')