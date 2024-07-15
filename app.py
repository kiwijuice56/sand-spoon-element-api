import os
from dotenv import load_dotenv

from flask import Flask, request

from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def get_custom_element():
    element_name = request.args.get("element_name")[:12]
    if len(element_name) == 0:
        return {}

    response = {}
    total_tokens = 0

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer in HEX format exactly"},
            {"role": "user", "content": f"Color of '{element_name}'"},
        ]
    )
    response["color_0"] = completion.choices[0].message.content
    total_tokens += completion.usage.total_tokens

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer in HEX format exactly"},
            {"role": "user", "content": f"Color of '{element_name}'"},
        ]
    )
    response["color_1"] = completion.choices[0].message.content
    total_tokens += completion.usage.total_tokens

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer only an exact entry from the list: [liquid, gas, rigid_solid, powdery_solid, life]"},
            {"role": "user", "content": f"Best description of '{element_name}'"}
        ]
    )
    response["state"] = completion.choices[0].message.content
    total_tokens += completion.usage.total_tokens

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer either Y or N exactly"},
            {"role": "user", "content": f"Is '{element_name}' flammable?"}
        ]
    )
    response["flammable"] = completion.choices[0].message.content
    total_tokens += completion.usage.total_tokens

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer either Y or N exactly"},
            {"role": "user", "content": f"Is '{element_name}' explosive?"}
        ]
    )
    response["explosive"] = completion.choices[0].message.content
    total_tokens += completion.usage.total_tokens

    print(total_tokens)
    print(response)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')