"""
Career Coach WhatsApp Bot - Webhook Enabled (Manual Registration)
FastAPI + PyWA with two-way communication for career coaching
"""

import logging
import os
import random
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pywa import WhatsApp, handlers, types

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Career Coach WhatsApp Bot",
    description="AI Career Coach with two-way WhatsApp communication",
    version="1.0.0",
)


# Pydantic models
class SendMessage(BaseModel):
    to: str
    message: str


# Career Coach responses
WELCOME_MESSAGES = [
    "Hello! I'm Coach Alex, your AI Career Advisor! 🚀\nHow can I help boost your career today?",
    "Hi there! Ready to level up your career? 💼\nWhat's your biggest career question right now?",
    "Welcome! I'm here to help with all things career-related! 🎯\nWhat would you like to discuss?",
]

# Initialize PyWA WITHOUT automatic webhook registration
wa = None
webhook_registered = False

try:
    phone_id = os.getenv("PHONE_ID")
    access_token = os.getenv("ACCESS_TOKEN")
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    verify_token = os.getenv("VERIFY_TOKEN")

    if not all([phone_id, access_token, app_id, app_secret]):
        missing = []
        if not phone_id:
            missing.append("PHONE_ID")
        if not access_token:
            missing.append("ACCESS_TOKEN")
        if not app_id:
            missing.append("APP_ID")
        if not app_secret:
            missing.append("APP_SECRET")
        if not verify_token:
            missing.append("VERIFY_TOKEN")

        logger.error(f"❌ Missing required environment variables: {missing}")
        logger.error("Check your .env file for WhatsApp API credentials!")

    else:
        # Initialize PyWA client WITHOUT webhook registration
        wa = WhatsApp(
            phone_id=str(phone_id),
            token=str(access_token),
            app_id=str(app_id),
            app_secret=str(app_secret),
            verify_token=str(verify_token),
            server=app,  # Connect to FastAPI but don't register webhooks yet
        )
        logger.info("✅ Career Coach WhatsApp client initialized (webhooks pending)")

except Exception as e:
    logger.error(f"❌ Failed to initialize WhatsApp client: {e}")
    logger.error("This usually means missing environment variables or wrong values")
    wa = None


# Message handlers - defined globally
def handle_incoming_message(client: WhatsApp, msg: types.Message):
    """Handle incoming WhatsApp messages"""
    user_name = msg.from_user.name or "Friend"
    user_message = msg.text or ""

    logger.info(f"📨 Received from {user_name}: {user_message}")

    try:
        # Test webhook
        if user_message.lower() in ["test", "ping", "webhook"]:
            msg.react("✅")
            msg.reply_text(
                f"🎉 **Webhook Working!**\n\n"
                f"✅ Message received: _{user_message}_\n"
                f"✅ From: {user_name}\n"
                f"✅ Two-way communication active!\n\n"
                f"I'm Coach Alex, ready to help with your career! 💼"
            )
            return

        # Greetings
        if user_message.lower() in ["hi", "hello", "hey", "hii", "start"]:
            welcome_msg = random.choice(WELCOME_MESSAGES)
            msg.react("👋")
            msg.reply_text(
                text=f"👋 Hey {user_name}!\n\n{welcome_msg}",
                buttons=[
                    types.Button(title="🎯 Career Goals", callback_data="goals"),
                    types.Button(title="📝 Resume Tips", callback_data="resume"),
                    types.Button(title="🔍 Job Search", callback_data="jobs"),
                ],
            )
            return

        # Career keywords
        career_keywords = [
            "job",
            "career",
            "work",
            "salary",
            "resume",
            "interview",
            "skills",
            "boss",
            "promotion",
        ]
        if any(keyword in user_message.lower() for keyword in career_keywords):
            msg.react("💡")

            if "resume" in user_message.lower():
                advice = """📝 **Resume Tips:**

✅ Keep it 1-2 pages maximum
✅ Use action verbs (Led, Created, Improved)
✅ Quantify achievements with numbers
✅ Tailor keywords to job descriptions
✅ Professional email & clean formatting

**What field are you in?** I can give more specific advice! 🎯"""

            elif "interview" in user_message.lower():
                advice = """🎤 **Interview Success:**

✅ Research the company thoroughly
✅ Practice STAR method responses
✅ Prepare thoughtful questions
✅ Dress appropriately
✅ Send thank you email within 24hrs

**What type of interview?** Phone, video, or in-person? 🤔"""

            elif "salary" in user_message.lower():
                advice = """💰 **Salary Negotiation:**

✅ Research market rates first
✅ Know your value & achievements  
✅ Let them make the first offer
✅ Negotiate total compensation package
✅ Stay professional and positive

**Current situation?** New job offer or asking for a raise? 📊"""

            else:
                advice = f"""💼 **Career Advice:**

Great question about "{user_message}"! Here's my take:

✅ **Set clear goals** - Where do you want to be?
✅ **Invest in skills** - What capabilities do you need?
✅ **Build your network** - Relationships open doors
✅ **Stay persistent** - Career growth takes time
✅ **Track progress** - Regular self-assessment

**Tell me more!** What's your specific situation? 🎯"""

            msg.reply_text(advice.strip())
            return

        # Default response
        msg.reply_text(
            f"Thanks for reaching out! 😊\n\n"
            f"I'm Coach Alex, your AI career advisor. I specialize in helping with:\n\n"
            f"• 🎯 Career planning & goals\n"
            f"• 📝 Resume & interview tips\n"
            f"• 💰 Salary negotiation\n"
            f"• 📈 Skill development\n"
            f"• 🔍 Job search strategies\n\n"
            f"What career topic can I help you with today?"
        )

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        msg.reply_text("Oops! I had a technical hiccup. Please try again! 🤖")


def handle_button_click(client: WhatsApp, btn: types.CallbackButton):
    """Handle button clicks"""
    logger.info(f"Button clicked: {btn.data}")

    responses = {
        "goals": """🎯 **Career Goal Setting:**

Let's create your career roadmap! Tell me:

• What's your current role?
• Where do you want to be in 2-5 years?
• What's most important to you? (money, impact, flexibility, etc.)
• What's your biggest career challenge right now?

The more specific you are, the better I can help! 🚀""",
        "resume": """📝 **Resume Optimization:**

I'd love to help make your resume shine! Share:

• What industry/field are you in?
• What types of roles are you targeting?
• How many years of experience do you have?
• Any specific resume challenges you're facing?

Let's get you noticed by recruiters! ✨""",
        "jobs": """🔍 **Job Search Strategy:**

Job hunting can be tough, but we'll get you there! Tell me:

• What type of roles are you looking for?
• How long have you been searching?
• What job search methods are you using?
• What's been your biggest obstacle?

Let's create a winning job search plan! 💪""",
    }

    response = responses.get(
        btn.data, "Great choice! Tell me more about what you need help with! 🤔"
    )
    btn.reply_text(response.strip())


# API endpoints
@app.get("/")
async def root():
    return {
        "message": "Career Coach WhatsApp Bot is running! 🤖",
        "status": "healthy",
        "mode": "manual-webhook" if wa else "failed",
        "bot_ready": wa is not None,
        "webhook_registered": webhook_registered,
        "coach": "Alex - AI Career Advisor",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if wa else "error",
        "bot_active": wa is not None,
        "webhook_active": webhook_registered,
        "mode": "two-way-communication",
        "framework": "FastAPI + PyWA",
    }


@app.post("/register-webhook")
async def register_webhook():
    """Manually register webhook after server is running"""
    global wa, webhook_registered

    if webhook_registered:
        return {"status": "already_registered", "message": "Webhook already registered"}

    callback_url = os.getenv("CALLBACK_URL")
    verify_token = os.getenv("VERIFY_TOKEN")
    phone_id = os.getenv("PHONE_ID")
    access_token = os.getenv("ACCESS_TOKEN")
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")

    if not all(
        [callback_url, verify_token, phone_id, access_token, app_id, app_secret]
    ):
        raise HTTPException(
            status_code=400,
            detail="All environment variables required for webhook registration",
        )

    try:
        # Reinitialize PyWA WITH webhook registration now that server is running
        wa = WhatsApp(
            phone_id=str(phone_id),
            token=str(access_token),
            app_id=str(app_id),
            app_secret=str(app_secret),
            server=app,
            callback_url=str(callback_url),
            verify_token=str(verify_token),
            webhook_challenge_delay=60,
        )

        # Register message handlers
        wa.add_handlers(
            handlers.MessageHandler(handle_incoming_message),
            handlers.CallbackButtonHandler(handle_button_click),
        )

        webhook_registered = True
        logger.info(f"✅ Webhook registered successfully: {callback_url}")
        logger.info("✅ Message handlers registered")

        return {
            "status": "success",
            "message": "Webhook and handlers registered successfully",
            "callback_url": callback_url,
            "webhook_active": True,
        }

    except Exception as e:
        logger.error(f"❌ Failed to register webhook: {e}")
        raise HTTPException(
            status_code=500, detail=f"Webhook registration failed: {str(e)}"
        )


@app.get("/webhook-test")
async def webhook_test():
    """Test if webhook is configured correctly"""
    return {
        "webhook_configured": wa is not None,
        "webhook_registered": webhook_registered,
        "callback_url": os.getenv("CALLBACK_URL"),
        "verify_token_set": bool(os.getenv("VERIFY_TOKEN")),
        "ready_for_messages": wa is not None and webhook_registered,
    }


@app.post("/send-message")
async def send_message(message_data: SendMessage):
    """Send a message via API"""
    if not wa:
        raise HTTPException(status_code=500, detail="WhatsApp client not initialized")

    try:
        result = wa.send_message(to=message_data.to, text=message_data.message)
        return {"status": "sent", "message_id": result.id}
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🤖 Starting Career Coach WhatsApp Bot (Manual Webhook)")
    print("=" * 60)

    # Check environment variables
    required_vars = ["PHONE_ID", "ACCESS_TOKEN", "APP_ID", "APP_SECRET"]
    webhook_vars = ["CALLBACK_URL", "VERIFY_TOKEN"]

    missing_required = [var for var in required_vars if not os.getenv(var)]
    missing_webhook = [var for var in webhook_vars if not os.getenv(var)]

    if missing_required:
        print(f"❌ Missing required variables: {missing_required}")
        print("\n📝 You need to add these to your .env file:")
        for var in missing_required:
            print(f"   {var}=your_{var.lower()}_value")
    else:
        print("✅ Required environment variables loaded")

    if missing_webhook:
        print(f"⚠️  Missing webhook variables: {missing_webhook}")
        print("   These are needed for two-way communication")
        for var in missing_webhook:
            if var == "CALLBACK_URL":
                print(f"   {var}=https://your-cloudflare-domain.com")
            elif var == "VERIFY_TOKEN":
                print(f"   {var}=your_custom_webhook_verify_token")

    if wa:
        print("✅ Career Coach bot initialized (send-only mode)")
        print("🔧 Call POST /register-webhook after server starts for two-way chat")
    else:
        print("❌ Bot initialization failed - check your .env file")

    print(f"\n🚀 Server starting on: http://localhost:{os.getenv('PORT', '8000')}")
    print("📊 After server starts:")
    print("   1. POST /register-webhook - Enable two-way communication")
    print("   2. GET /webhook-test - Test webhook status")
    print("   3. GET /health - Check bot health")

    uvicorn.run(
        "career_coach_webhook:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
        log_level="info",
    )
