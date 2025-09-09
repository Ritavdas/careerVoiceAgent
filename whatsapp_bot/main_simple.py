"""
Simple WhatsApp Bot - Send Only Mode
FastAPI + PyWA for sending messages only (no webhooks)
"""

import logging
import os
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pywa import WhatsApp

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="WhatsApp Bot - Send Only",
    description="Simple WhatsApp Bot for sending messages",
    version="1.0.0",
)


# Pydantic models
class SendMessage(BaseModel):
    to: str
    message: str


class BroadcastMessage(BaseModel):
    message: str
    recipients: list[str]


# Initialize PyWA in send-only mode (no webhook)
wa = None
try:
    phone_id = os.getenv("PHONE_ID")
    access_token = os.getenv("ACCESS_TOKEN")

    if not phone_id or not access_token:
        logger.error("❌ PHONE_ID or ACCESS_TOKEN missing in .env file")
    else:
        wa = WhatsApp(
            phone_id=phone_id,
            token=access_token,
            # No server/webhook parameters = send-only mode
        )
        logger.info("✅ WhatsApp client initialized successfully (send-only mode)")
except Exception as e:
    logger.error(f"❌ Failed to initialize WhatsApp client: {e}")
    logger.error("Check your PHONE_ID and ACCESS_TOKEN in .env file")


# API endpoints
@app.get("/")
async def root():
    return {
        "message": "WhatsApp Bot is running! 🤖",
        "status": "healthy",
        "mode": "send-only",
        "bot_ready": wa is not None,
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if wa else "error",
        "bot_active": wa is not None,
        "mode": "send-only",
        "framework": "FastAPI + PyWA",
    }


@app.post("/send-message")
async def send_message(message_data: SendMessage):
    """Send a message to a specific WhatsApp number"""
    if not wa:
        raise HTTPException(
            status_code=500,
            detail="WhatsApp client not initialized. Check your credentials in .env file.",
        )

    try:
        logger.info(f"Sending message to {message_data.to}: {message_data.message}")

        result = wa.send_message(to=message_data.to, text=message_data.message)

        logger.info(f"✅ Message sent successfully. ID: {result.id}")
        return {"status": "sent", "message_id": result.id, "to": message_data.to}

    except Exception as e:
        logger.error(f"❌ Failed to send message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/broadcast")
async def broadcast_message(broadcast: BroadcastMessage):
    """Send message to multiple recipients"""
    if not wa:
        raise HTTPException(status_code=500, detail="WhatsApp client not initialized")

    results = []
    for recipient in broadcast.recipients:
        try:
            result = wa.send_message(to=recipient, text=broadcast.message)
            results.append(
                {"recipient": recipient, "status": "sent", "message_id": result.id}
            )
            logger.info(f"✅ Message sent to {recipient}")

        except Exception as e:
            logger.error(f"❌ Failed to send to {recipient}: {e}")
            results.append(
                {"recipient": recipient, "status": "failed", "error": str(e)}
            )

    return {"results": results}


@app.get("/test-credentials")
async def test_credentials():
    """Test if your credentials are working"""
    phone_id = os.getenv("PHONE_ID")
    access_token = os.getenv("ACCESS_TOKEN")
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")

    credentials = {
        "phone_id": phone_id,
        "access_token": access_token[:10] + "..." if access_token else None,
        "app_id": app_id,
        "app_secret": app_secret[:5] + "..." if app_secret else None,
    }

    missing = []
    if not phone_id:
        missing.append("PHONE_ID")
    if not access_token:
        missing.append("ACCESS_TOKEN")

    return {
        "credentials_loaded": len(missing) == 0,
        "missing_credentials": missing,
        "bot_initialized": wa is not None,
        "ready_to_send": wa is not None and len(missing) == 0,
    }


if __name__ == "__main__":
    print("🤖 Starting WhatsApp Bot (Send-Only Mode)")
    print("=" * 50)

    # Check credentials on startup
    required_vars = ["PHONE_ID", "ACCESS_TOKEN"]
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print(f"❌ Missing environment variables: {missing}")
        print("Please check your .env file!")
    else:
        print("✅ Environment variables loaded")

    if wa:
        print("✅ WhatsApp client ready")
    else:
        print("❌ WhatsApp client failed to initialize")

    print("🚀 Starting server on http://localhost:8000")
    print("📊 Health check: http://localhost:8000/health")
    print("📚 API docs: http://localhost:8000/docs")

    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
        log_level="info",
    )
