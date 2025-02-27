from fastapi import APIRouter, Request, HTTPException, Form
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from models.user_model import FirstMessage

load_dotenv()

router = APIRouter()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# 📌 1️⃣ First Message API - Sends Terms & Conditions
@router.post("/first-message")
def send_first_message(data: FirstMessage):
    try:
        message_text = """MOON is a supportive AI companion, not a licensed therapist or mental health
professional. It does not replace professional therapy or medical advice. By
continuing, you confirm that you are over 18 years old and agree to use MOON
as a self-reflection and support tool."""

        # message = client.messages.create(
        #     body=message_text,
        #     from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
        #     to=f"whatsapp:{data.phone_number}"
        # )

        return {"message": "Agreement message sent!", "sid": 'message.sid'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📌 2️⃣ Twilio Webhook API - Receives & Responds to Messages
@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    from_number = form.get("From")
    message_body = form.get("Body").strip().lower()

    print(f"Received from {from_number}: {message_body}")

    # response = MessagingResponse()

    if message_body == "yes":
        # response.message("Thank you for accepting the terms! How can we assist you?")
        pass
    elif message_body == "no":
        # response.message("You need to accept the terms to continue. Reply 'YES' to proceed.")
        pass
    else:
        # response.message("I'm here to assist you. Please type 'YES' to accept terms or ask any questions.")
        pass

    response = "test response"
    return str(response)