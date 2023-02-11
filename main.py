from flask import Flask, request
import os
import openai
from flask_cors import CORS

import sys
import json

app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')  # this is the home page route
def hello_world():  # this is the home page function that generates the page code
    return "Hello world!"



@app.route('/webhook', methods=['POST'])
def get_response():
    prompt = "The following is a conversation with a therapist and a user. The therapist is JOY, who uses compassionate listening to have helpful and meaningful conversations with users. JOY is empathic and friendly. JOY's objective is to make the user feel better by feeling heard. With each response, JOY offers follow-up questions to encourage openness and tries to continue the conversation in a natural way. Joy doesn't send more than one response after the user's text\n\nJOY-> Hello, I am your personal mental health assistant. What's on your mind today?\nUser->"
    print(prompt)
    r = (request.args if request.args else request.json)
    query = r['query']
    prev_data = r['prev_data']
    context = prev_data + "User->" + query + "JOY->"
    
    try:
        response = openai.Completion.create(
            model="davinci:ft-personal-2023-02-10-08-28-43",
            prompt=prompt+context,
            temperature=0.89,
            max_tokens=162,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" END", "JOY->", "User->", "user->"]
        )
        answer = response.get('choices')[0].get('text')
        previous_response = context + "JOY-> " + answer
        result = {"answer": str(answer), "new_prev_data": str(previous_response)}
#         result_json = json.dumps(result, indent = 4)
        return json.dumps(result, indent = 4)
    except Exception as e:
        print('error',e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return ('oops',exc_type, fname, exc_tb.tb_lineno)
        return '400'


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = os.getenv("PORT")) # run the flask app on debug mode

