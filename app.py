import os
from dotenv import load_dotenv

from flask import Flask, request
from flask_cors import CORS

from openai import OpenAI

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def get_custom_element():
    element_name = request.args.get("element_name")[:12]
    if len(element_name) == 0:
        return {}


    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer in hex only"},
            {"role": "user", "content": f"Color of: {element_name}"}
        ]
    )

    return {"color": completion.choices[0].message.content}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')