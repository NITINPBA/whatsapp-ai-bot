import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

@app.route("/")
def home():
    return "WhatsApp AI Bot Running"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_message = request.form.get("Body", "")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a helpful WhatsApp assistant.

Keep replies:
- Short
- Friendly
- Professional
- Natural
"""
            },
            {
                "role": "user",
                "content": incoming_message
            }
        ],
        temperature=0.5
    )

    reply = response.choices[0].message.content

    twilio_response = MessagingResponse()
    twilio_response.message(reply)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
