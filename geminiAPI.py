
import google.generativeai as genai
from flask import jsonify,request
from __main__ import app, db
from fastapi.encoders import jsonable_encoder

def get_api_key():
    return "AIzaSyDnS5Ri7GxcYEU4Jk3Iidlj0Zh4kQscTUI" 

genai.configure(api_key=get_api_key())

model = genai.GenerativeModel('gemini-1.5-pro-latest')


chat_session = model.start_chat(history=[])
next_message = ""
next_image = ""
description = ""  # Initialize description variable




@app.route("/api/geminiAPI/<string:message>", methods=["GET","POST"])
def chat(message):
    message="summarize this:boys in need"


    # Configure the model using the retrieved API key
    genai.configure(api_key=get_api_key())

    # The rate limits are low on this model, so you might need to switch to gemini-pro
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    chat_session = model.start_chat(history=[])

    try:
        response = chat_session.send_message(chat_session.history + [message], stream=False)
        return jsonify(success=True, message=response.text)
    except Exception as e:
        print(f"Error sending message: {e}")
        return jsonify(success=False, message="Error processing message")

