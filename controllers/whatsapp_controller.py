from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

from models.database import SessionLocal
from models.user_model import User
from models.conversation_model import Conversation
from models.message_model import FirstMessage

# Load environment variables
load_dotenv()

router = APIRouter()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📌 1️⃣ First Message API - Sends Terms & Conditions & Saves User
@router.post("/first-message")
def send_first_message(data: FirstMessage, db: Session = Depends(get_db)):
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.phone_number == data.phone_number).first()
        if not existing_user:
            new_user = User(phone_number=data.phone_number, name=data.name, interest=data.interest)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        message_text = (
            f"Hello {data.name},\n"
            f"We see that you're interested in {data.interest}. "
            "Please accept our terms & conditions by replying 'YES'."
        )

        # message = client.messages.create(
        #     body=message_text,
        #     from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
        #     to=f"whatsapp:{data.phone_number}"
        # )

        return {"message": "Agreement message sent!", "sid": "message.sid"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 📌 2️⃣ Twilio Webhook API - Receives & Stores Messages
@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    from_number = form.get("From").replace("whatsapp:", "").strip()
    message_body = form.get("Body").strip()

    user = db.query(User).filter(User.phone_number == from_number).first()
    if not user:
        return "User not found"

    new_conversation = Conversation(user_id=user.id, user_messages=message_body)
    db.add(new_conversation)
    db.commit()

    response = MessagingResponse()
    if message_body.lower() == "yes":
        response.message("Thank you for accepting the terms! How can we assist you?")
    elif message_body.lower() == "no":
        response.message("You need to accept the terms to continue. Reply 'YES' to proceed.")
    else:
        response.message("I'm here to assist you. Please type 'YES' to accept terms.")

    return str(response)