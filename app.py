import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Add only the WhatsApp numbers allowed to use your bot.
# Format must be: whatsapp:+countrycode_number
ALLOWED_NUMBERS = [
    "whatsapp:+918446451617",
    "whatsapp:+918108661602",
]

@app.route("/")
def home():
    return "WhatsApp AI Bot Running"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_message = request.form.get("Body", "")
    sender_number = request.form.get("From", "")

    # Block anyone not in your approved list
    if sender_number not in ALLOWED_NUMBERS:
        twilio_response = MessagingResponse()
        twilio_response.message("This bot is currently available only for approved contacts.")
        return str(twilio_response)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are Nitin's business assistant.

Rules:
- Always reply in the same language used by the sender.
- If the sender writes in Marathi, reply in Marathi.
- If the sender writes in Hindi, reply in Hindi.
- If the sender writes in English, reply in English.
- Keep replies short and natural like WhatsApp messages.
- Sound friendly and professional.
- Do not write long paragraphs.
- Ask only one question at a time.
"""
            },
            {"role": "user", "content": incoming_message}
        ],
        temperature=0.5
    )

    reply = response.choices[0].message.content

    twilio_response = MessagingResponse()
    twilio_response.message(reply)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
