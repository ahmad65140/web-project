
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




@app.route("/api/geminiAPI", methods=["GET","POST"])
def chat():
    message="summarize this very breaifly in two sentences: audi league clubs are targeting signing a number of Premier League clubs during the current summer transfer window, including Liverpool duo Mohamed Salah and Brazilian goalkeeper Alisson Becker.The British newspaper «Telegraph»: «Saudi League targets the contract with Liverpool goalkeeper Alisson, and Ederson goalkeeper Manchester City».The newspaper added: It is known ther is strong interest from the Saudi league to sign Mohamed Salah, who received a £150m offer last year from the federation, and the file will be reopened this summerA number of press reports indicate the possibility of the departure of Mohamed Salah from the ranks of Liverpool, during the current summer transfer period, especially with the change of the technical staff of the Reds and the departure of German Jurgen Klopp."


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

