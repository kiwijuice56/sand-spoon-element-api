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

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer in hex format"},
            {"role": "user", "content": f"Main color of: {element_name}"},
        ]
    )
    response["color_0"] = completion.choices[0].message.content

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer in hex format"},
            {"role": "user", "content": f"Secondary color of: {element_name}"},
        ]
    )
    response["color_1"] = completion.choices[0].message.content

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer in 1 word"},
            {"role": "user", "content": f"From this list of choices: [liquid, gas, rigid_solid, powdery_solid, life], pick the best description of {element_name}"}
        ]
    )
    response["state"] = completion.choices[0].message.content

    print(response)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')