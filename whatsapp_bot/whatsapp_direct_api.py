"""
WhatsApp Business API Direct Implementation
Career Coach Bot - No PyWA, Direct Meta API calls
Clean, simple, transparent webhook handling
"""

import hashlib
import hmac
import json
import logging
import os
import random
from typing import Any, Dict, Optional

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request, Response
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="WhatsApp Career Coach Bot - Direct API",
    description="Direct WhatsApp Business API implementation",
    version="2.0.0",
)

# Configuration from environment
PHONE_ID = os.getenv("PHONE_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
APP_SECRET = os.getenv("APP_SECRET")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "career_coach_verify_token")
GRAPH_API_URL = "https://graph.facebook.com/v18.0"

# Validate required environment variables
if not all([PHONE_ID, ACCESS_TOKEN, APP_SECRET, VERIFY_TOKEN]):
    logger.error("Missing required environment variables!")
    logger.error(f"PHONE_ID: {'✓' if PHONE_ID else '✗'}")
    logger.error(f"ACCESS_TOKEN: {'✓' if ACCESS_TOKEN else '✗'}")
    logger.error(f"APP_SECRET: {'✓' if APP_SECRET else '✗'}")
    logger.error(f"VERIFY_TOKEN: {'✓' if VERIFY_TOKEN else '✗'}")


# ============= MODELS =============
class SendMessage(BaseModel):
    """Model for sending messages via API"""

    to: str
    message: str


# ============= CAREER COACH RESPONSES =============
WELCOME_MESSAGES = [
    "Hello! I'm Coach Alex, your AI Career Advisor! 🚀\nHow can I help boost your career today?",
    "Hi there! Ready to level up your career? 💼\nWhat's your biggest career question right now?",
    "Welcome! I'm here to help with all things career-related! 🎯\nWhat would you like to discuss?",
]

CAREER_ADVICE = {
    "resume": """📝 **Resume Tips:**

✅ Keep it 1-2 pages maximum
✅ Use action verbs (Led, Created, Improved)
✅ Quantify achievements with numbers
✅ Tailor keywords to job descriptions
✅ Professional email & clean formatting

**What field are you in?** I can give more specific advice! 🎯""",
    "interview": """🎤 **Interview Success:**

✅ Research the company thoroughly
✅ Practice STAR method responses
✅ Prepare thoughtful questions
✅ Dress appropriately
✅ Send thank you email within 24hrs

**What type of interview?** Phone, video, or in-person? 🤔""",
    "salary": """💰 **Salary Negotiation:**

✅ Research market rates first
✅ Know your value & achievements
✅ Let them make the first offer
✅ Negotiate total compensation package
✅ Stay professional and positive

**Current situation?** New job offer or asking for a raise? 📊""",
}


# ============= WEBHOOK VERIFICATION (GET) =============
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """
    Handle webhook verification from Meta
    Meta sends: GET /webhook?hub.mode=subscribe&hub.challenge=CHALLENGE&hub.verify_token=TOKEN
    """
    logger.info(
        f"Webhook verification request: mode={hub_mode}, token={hub_verify_token}"
    )

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        logger.info("✅ Webhook verified successfully")
        # Return the challenge as plain text integer
        return Response(content=hub_challenge, media_type="text/plain")

    logger.error(f"❌ Webhook verification failed: token mismatch or wrong mode")
    raise HTTPException(status_code=403, detail="Verification failed")


# ============= WEBHOOK MESSAGE RECEIVER (POST) =============
@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Handle incoming messages from WhatsApp
    """
    # Get the request body
    body = await request.json()

    # Log the incoming webhook
    logger.info(f"📨 Received webhook: {json.dumps(body, indent=2)}")

    # Verify webhook signature (optional but recommended)
    if APP_SECRET:
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not verify_webhook_signature(await request.body(), signature):
            logger.error("❌ Invalid webhook signature")
            raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        # Process the webhook
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})

                    # Get phone number ID for replies
                    phone_number_id = value.get("metadata", {}).get("phone_number_id")

                    # Process messages
                    messages = value.get("messages", [])
                    for message in messages:
                        await process_message(message, phone_number_id)

                    # Process status updates (optional)
                    statuses = value.get("statuses", [])
                    for status in statuses:
                        logger.info(
                            f"📊 Status update: {status.get('status')} for {status.get('recipient_id')}"
                        )

    except Exception as e:
        logger.error(f"❌ Error processing webhook: {e}")

    # Always return 200 OK to acknowledge receipt
    return {"status": "EVENT_RECEIVED"}


# ============= MESSAGE PROCESSOR =============
async def process_message(message: Dict[str, Any], phone_number_id: Optional[str]):
    """
    Process incoming WhatsApp messages
    """
    sender = message.get("from")
    message_type = message.get("type")
    message_id = message.get("id")

    logger.info(f"Processing {message_type} message from {sender}")

    # Handle different message types
    if message_type == "text":
        text_body = message.get("text", {}).get("body", "")
        if sender:
            await handle_text_message(sender, text_body, phone_number_id)

    elif message_type == "interactive":
        # Handle button/list replies
        interactive = message.get("interactive", {})
        if interactive.get("type") == "button_reply":
            button_id = interactive.get("button_reply", {}).get("id")
            if sender:
                await handle_button_reply(sender, button_id, phone_number_id)

    elif message_type == "request_welcome":
        # First time message from user
        if sender:
            await send_welcome_message(sender, phone_number_id)

    else:
        logger.info(f"Received {message_type} message - not processed")


# ============= MESSAGE HANDLERS =============
async def handle_text_message(sender: str, text: str, phone_number_id: Optional[str]):
    """
    Handle incoming text messages
    """
    text_lower = text.lower()

    # Test webhook
    if text_lower in ["test", "ping", "webhook"]:
        await send_text_message(
            sender,
            f"🎉 **Webhook Working!**\n\n"
            f"✅ Message received: _{text}_\n"
            f"✅ Two-way communication active!\n\n"
            f"I'm Coach Alex, ready to help with your career! 💼",
            phone_number_id,
        )
        return

    # Greetings
    if any(greeting in text_lower for greeting in ["hi", "hello", "hey", "start"]):
        await send_welcome_message(sender, phone_number_id)
        return

    # Career keywords
    if "resume" in text_lower:
        if phone_number_id:
            await send_text_message(sender, CAREER_ADVICE["resume"], phone_number_id)
    elif "interview" in text_lower:
        if phone_number_id:
            await send_text_message(sender, CAREER_ADVICE["interview"], phone_number_id)
    elif "salary" in text_lower or "negotiat" in text_lower:
        if phone_number_id:
            await send_text_message(sender, CAREER_ADVICE["salary"], phone_number_id)
    elif any(
        word in text_lower for word in ["job", "career", "work", "skills", "promotion"]
    ):
        if phone_number_id:
            await send_career_advice(sender, text, phone_number_id)
    else:
        if phone_number_id:
            await send_default_message(sender, phone_number_id)


async def handle_button_reply(sender: str, button_id: str, phone_number_id: Optional[str]):
    """
    Handle button click responses
    """
    responses = {
        "goals": """🎯 **Career Goal Setting:**

Let's create your career roadmap! Tell me:
• What's your current role?
• Where do you want to be in 2-5 years?
• What's most important to you?
• What's your biggest challenge?

The more specific, the better I can help! 🚀""",
        "resume": CAREER_ADVICE["resume"],
        "jobs": """🔍 **Job Search Strategy:**

Job hunting can be tough! Tell me:
• What roles are you targeting?
• How long have you been searching?
• What methods are you using?
• What's been your biggest obstacle?

Let's create a winning plan! 💪""",
    }

    response = responses.get(
        button_id, "Great choice! Tell me more about what you need help with! 🤔"
    )
    if phone_number_id:
        await send_text_message(sender, response, phone_number_id)


# ============= MESSAGE SENDERS =============
async def send_text_message(to: str, text: str, phone_number_id: Optional[str]) -> bool:
    """
    Send a text message via WhatsApp API
    """
    if not phone_number_id:
        logger.error("No phone_number_id provided for text message")
        return False

    url = f"{GRAPH_API_URL}/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info(f"✅ Message sent to {to}")
            return True
        else:
            logger.error(f"❌ Failed to send message: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Error sending message: {e}")
        return False


async def send_button_message(
    to: str, text: str, buttons: list, phone_number_id: Optional[str]
) -> bool:
    """
    Send an interactive button message
    """
    if not phone_number_id:
        logger.error("No phone_number_id provided for button message")
        return False

    url = f"{GRAPH_API_URL}/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": btn["id"], "title": btn["title"]}}
                    for btn in buttons
                ]
            },
        },
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info(f"✅ Button message sent to {to}")
            return True
        else:
            logger.error(f"❌ Failed to send button message: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Error sending button message: {e}")
        return False


async def send_welcome_message(to: str, phone_number_id: Optional[str]):
    """
    Send welcome message with buttons
    """
    if not phone_number_id:
        logger.error("No phone_number_id provided for welcome message")
        return

    welcome_text = random.choice(WELCOME_MESSAGES)
    buttons = [
        {"id": "goals", "title": "🎯 Career Goals"},
        {"id": "resume", "title": "📝 Resume Tips"},
        {"id": "jobs", "title": "🔍 Job Search"},
    ]
    await send_button_message(to, welcome_text, buttons, phone_number_id)


async def send_career_advice(to: str, user_message: str, phone_number_id: Optional[str]):
    """
    Send general career advice
    """
    if not phone_number_id:
        logger.error("No phone_number_id provided for career advice")
        return

    advice = f"""💼 **Career Advice:**

Great question about "{user_message[:50]}..."! Here's my take:

✅ **Set clear goals** - Where do you want to be?
✅ **Invest in skills** - What capabilities do you need?
✅ **Build your network** - Relationships open doors
✅ **Stay persistent** - Career growth takes time
✅ **Track progress** - Regular self-assessment

**Tell me more!** What's your specific situation? 🎯"""

    await send_text_message(to, advice, phone_number_id)


async def send_default_message(to: str, phone_number_id: Optional[str]):
    """
    Send default response
    """
    message = """Thanks for reaching out! 😊

I'm Coach Alex, your AI career advisor. I can help with:

• 🎯 Career planning & goals
• 📝 Resume & interview tips
• 💰 Salary negotiation
• 📈 Skill development
• 🔍 Job search strategies

What career topic can I help you with today?"""

    await send_text_message(to, message, phone_number_id)


# ============= WEBHOOK SIGNATURE VERIFICATION =============
def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify webhook signature from Meta
    """
    if not signature or not APP_SECRET:
        return False

    try:
        # Remove 'sha256=' prefix
        signature = signature.replace("sha256=", "")

        # Calculate expected signature
        expected_signature = hmac.new(
            APP_SECRET.encode(), payload, hashlib.sha256
        ).hexdigest()

        # Compare signatures
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Error verifying signature: {e}")
        return False


# ============= API ENDPOINTS =============
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "WhatsApp Career Coach Bot - Direct API",
        "status": "healthy",
        "webhook_url": "/webhook",
        "environment": {
            "phone_id": "✓" if PHONE_ID else "✗",
            "access_token": "✓" if ACCESS_TOKEN else "✗",
            "app_secret": "✓" if APP_SECRET else "✗",
            "verify_token": "✓" if VERIFY_TOKEN else "✗",
        },
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_version": "v18.0",
        "webhook_path": "/webhook",
        "ready": all([PHONE_ID, ACCESS_TOKEN, VERIFY_TOKEN]),
    }


@app.post("/send-message")
async def send_message_api(message: SendMessage):
    """API endpoint to send messages"""
    if not all([PHONE_ID, ACCESS_TOKEN]):
        raise HTTPException(status_code=500, detail="Missing configuration")

    if not PHONE_ID:
        raise HTTPException(status_code=500, detail="PHONE_ID not configured")

    success = await send_text_message(message.to, message.message, PHONE_ID)
    if success:
        return {"status": "sent", "to": message.to}
    else:
        raise HTTPException(status_code=500, detail="Failed to send message")


@app.get("/test-webhook")
async def test_webhook():
    """Test webhook configuration"""
    return {
        "webhook_url": "/webhook",
        "verify_token_configured": bool(VERIFY_TOKEN),
        "app_secret_configured": bool(APP_SECRET),
        "phone_id_configured": bool(PHONE_ID),
        "access_token_configured": bool(ACCESS_TOKEN),
        "instructions": {
            "1": "Configure webhook URL in Meta Dashboard: https://your-domain.com/webhook",
            "2": f"Use this verify token: {VERIFY_TOKEN}",
            "3": "Subscribe to 'messages' field",
            "4": "Test by sending a WhatsApp message to your business number",
        },
    }


# ============= MAIN =============
if __name__ == "__main__":
    print("🚀 WhatsApp Career Coach Bot - Direct API Implementation")
    print("=" * 60)

    # Check configuration
    if not all([PHONE_ID, ACCESS_TOKEN, APP_SECRET, VERIFY_TOKEN]):
        print("❌ Missing required environment variables:")
        if not PHONE_ID:
            print("  - PHONE_ID")
        if not ACCESS_TOKEN:
            print("  - ACCESS_TOKEN")
        if not APP_SECRET:
            print("  - APP_SECRET")
        if not VERIFY_TOKEN:
            print("  - VERIFY_TOKEN")
        print("\n📝 Add these to your .env file")
    else:
        print("✅ All environment variables loaded")

    print(f"\n📍 Webhook endpoint: /webhook")
    print(f"🔑 Verify token: {VERIFY_TOKEN}")
    print(f"\n🌐 Starting server on http://localhost:{os.getenv('PORT', '8000')}")
    print("\n📋 Next steps:")
    print("1. Start this server")
    print("2. Configure webhook URL in Meta Dashboard")
    print("3. Use the verify token shown above")
    print("4. Subscribe to 'messages' webhook field")
    print("5. Send a test message to your WhatsApp Business number")

    uvicorn.run(
        "whatsapp_direct_api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
        log_level="info",
    )
