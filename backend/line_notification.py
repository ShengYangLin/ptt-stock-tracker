import requests
import os
import base64
import datetime
from backend.db import request_updated_post, update_post_status

def send(message):
    line_token = os.getenv('LINE_TOKEN')
    headers = { "Authorization": "Bearer " + line_token }
    data = { 'message': message }
    requests.post("https://notify-api.line.me/api/notify", headers = headers, data = data)

def send_message():
    request_data = request_updated_post()
    for data in request_data:
        url = data["url"]
        encoded_pushes = data["pushes"]
        decoded_pushes = base64.b64decode(encoded_pushes).decode("utf8")
        message = f"https://www.ptt.cc/bbs/Stock{url}\n"
        push_text = ""
        for index, push in enumerate(decoded_pushes.split("\n")):
            if index != 0 and index % 10 == 0:
                send(message + push_text)
                push_text = ""
            else:
                push_text += push + "\n"
        if push_text != "":
            send(message + push_text)
        update_post_status(url)
    send(f"PTT Stock at {datetime.datetime.today()}.")
    print("Finish Sending.")

