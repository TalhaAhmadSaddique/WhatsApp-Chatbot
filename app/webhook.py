import os
from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder

from app.whatsapp_client import WhatsAppClient
from app.openai_client import OpenAIClient
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

WHATSAPP_HOOK_TOKEN = os.getenv("WHATSAPP_HOOK_TOKEN")

@app.get("/")
def get():
    return "Hello World!!"

@app.get("/webhook/")
def subscribe(request: Request):
    if request.query_params.get('hub.verify_token') == WHATSAPP_HOOK_TOKEN:
        return int(request.query_params.get('hub.challenge'))
    return "Authentication failed. Invalid Token."

@app.post("/webhook/")
async def process_notifications(request: Request):
    wtsapp_client = WhatsAppClient()
    data = await request.json()
    print ("We received " + str(data))
    response = wtsapp_client.process_notification(data)
    if response["statusCode"] == 200:
        if response["body"] and response["from_no"]:
            openai_client = OpenAIClient()
            reply = openai_client.chatbot(prompt=response["body"])
            print ("\nreply is:"  + reply)
            wtsapp_client.send_text_message(message=reply, phone_number=response["from_no"], )
            print ("\nreply is sent to whatsapp cloud:" + str(response))

    return jsonable_encoder({"status": "success"}, 200)