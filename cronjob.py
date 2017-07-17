# coding=utf-8
import os
import sys
import json

import requests
from flask import Flask, request
#from models import from models.usarios

app = Flask(__name__)

#recibe un cluster y envía un mensaje
def getUsers(cluster):
    usuarios = Oferta2.objects.filter(cluster=cluster)
    for usuarios in usuarios:
        webhookCRONJOB(usuarios.sender_id, usuarios.recipient_id)

def webhookCRONJOB(sender_id, recipient_id ):

    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):

                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]

                    #conversación de envío vía cronjob

                    if (message_text == "Hola"):
                        send_message(sender_id, "Esto lo mandamos a los que ya están suscritos")


                if messaging_event.get("delivery"):  # eventos posteriores
                       pass

                if messaging_event.get("optin"):  # cofirmación optin
                       pass
                if messaging_event.get("postback"):  # postbacks
                       pass


    return "ok", 200

#definicion del envío con plantillas genericas de mensajes
def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)



def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
