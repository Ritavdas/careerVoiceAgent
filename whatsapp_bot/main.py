"""
Simple WhatsApp Bot using FastAPI + PyWA
A basic bot with essential features to get you started.
"""

import logging
import os
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pywa import WhatsApp, filters, types

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="WhatsApp Bot",
    description="Simple WhatsApp Bot built with FastAPI + PyWA",
    version="1.0.0",
)


# Pydantic models for API endpoints
class BroadcastMessage(BaseModel):
    message: str
    recipients: list[str]


class SendMessage(BaseModel):
    to: str
    message: str


# Initialize PyWA WITHOUT webhook/server integration (send-only mode)
try:
    wa = WhatsApp(
        phone_id=os.getenv("PHONE_ID"),
        token=os.getenv("ACCESS_TOKEN"),
        # Removed server, callback_url, verify_token for send-only mode
        app_id=int(os.getenv("APP_ID", "0")),
        app_secret=os.getenv("APP_SECRET"),
    )
    logger.info("WhatsApp client initialized successfully (send-only mode)")
except Exception as e:
    logger.error(f"Failed to initialize WhatsApp client: {e}")
    wa = None


# API Health Check
@app.get("/")
async def root():
    return {
        "message": "WhatsApp Bot is running! 🤖",
        "status": "healthy",
        "framework": "FastAPI + PyWA",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if wa else "error",
        "bot_active": wa is not None,
        "framework": "FastAPI + PyWA",
    }


# API endpoint to send messages
@app.post("/send-message")
async def send_message(message_data: SendMessage):
    """Send a message to a specific WhatsApp number"""
    if not wa:
        raise HTTPException(status_code=500, detail="WhatsApp client not initialized")

    try:
        result = wa.send_message(to=message_data.to, text=message_data.message)
        return {"status": "sent", "message_id": result.id}
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
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
        except Exception as e:
            logger.error(f"Failed to send to {recipient}: {e}")
            results.append(
                {"recipient": recipient, "status": "failed", "error": str(e)}
            )

    return {"results": results}


# Bot Event Handlers
if wa:

    @wa.on_message
    def handle_message(client: WhatsApp, msg: types.Message):
        """Handle all incoming messages"""
        logger.info(f"Received message from {msg.from_user.name}: {msg.text}")

        # Welcome/Greeting handler
        if msg.text and msg.text.lower() in ["hi", "hello", "hey", "start"]:
            msg.react("👋")
            welcome_text = f"""
Hello {msg.from_user.name}! 👋

Welcome to our WhatsApp Bot! 🤖

**Available Commands:**
• `hi/hello` - Get this welcome message
• `help` - Show help information  
• `ping` - Test bot response
• `menu` - Show available options
• Math expressions (e.g., `5 + 3`) - Calculator

**Features:**
✅ Interactive buttons
✅ Built-in calculator
✅ Image processing
✅ Fast responses

Type `help` for more information!
            """

            msg.reply_text(
                text=welcome_text.strip(),
                buttons=[
                    types.Button(title="📋 Menu", callback_data="show_menu"),
                    types.Button(title="🆘 Help", callback_data="show_help"),
                    types.Button(title="🧮 Calculator", callback_data="show_calc"),
                ],
            )

        # Help command
        elif msg.text and msg.text.lower() in ["help", "/help"]:
            help_text = """
🤖 **Bot Help & Commands**

**💬 Basic Commands:**
• `hi/hello` - Welcome message
• `ping` - Test response
• `help` - This help message
• `menu` - Show options

**🧮 Calculator:**
Send math expressions like:
• `15 + 25` = 40
• `100 - 50` = 50  
• `12 * 8` = 96
• `144 / 12` = 12

**🎯 Features:**
• Interactive buttons
• Image processing
• Fast API endpoints
• Real-time responses

**🔧 Tech Stack:**
FastAPI + PyWA + WhatsApp Cloud API

Need help? Just ask! 😊
            """
            msg.reply_text(help_text.strip())

        # Ping command
        elif msg.text and msg.text.lower() == "ping":
            msg.react("🏓")
            msg.reply("🏓 Pong! Bot is working perfectly! ✅")

        # Menu command
        elif msg.text and msg.text.lower() == "menu":
            show_main_menu(msg)

        # Default response for unrecognized messages
        else:
            if msg.text:  # Only respond to text messages
                msg.reply_text(
                    f"I received: *{msg.text}*\n\n"
                    "I'm still learning! 🧠\n"
                    "Type `help` to see what I can do! 😊"
                )

    def show_main_menu(msg: types.Message):
        """Show the main interactive menu"""
        msg.reply_text(
            text="📋 **Main Menu** 📋\n\nWhat would you like to do?",
            buttons=types.SectionList(
                button_title="🚀 Choose Option",
                sections=[
                    types.Section(
                        title="🤖 Bot Features",
                        rows=[
                            types.SectionRow(
                                title="🧮 Calculator",
                                description="Perform math calculations",
                                callback_data="feature:calculator",
                            ),
                            types.SectionRow(
                                title="🆘 Help",
                                description="Get help and commands",
                                callback_data="feature:help",
                            ),
                            types.SectionRow(
                                title="ℹ️ About",
                                description="About this bot",
                                callback_data="feature:about",
                            ),
                        ],
                    ),
                    types.Section(
                        title="🎯 Quick Actions",
                        rows=[
                            types.SectionRow(
                                title="🏓 Ping Test",
                                description="Test bot response",
                                callback_data="action:ping",
                            ),
                            types.SectionRow(
                                title="📊 Bot Status",
                                description="Check bot health",
                                callback_data="action:status",
                            ),
                        ],
                    ),
                ],
            ),
        )

    # Handle button clicks
    @wa.on_callback_button
    def handle_button_click(client: WhatsApp, btn: types.CallbackButton):
        """Handle button interactions"""
        logger.info(f"Button clicked: {btn.data}")

        if btn.data == "show_menu":
            show_main_menu(btn)
        elif btn.data == "show_help":
            btn.reply_text("Type `help` to see all available commands! 🆘")
        elif btn.data == "show_calc":
            btn.reply_text(
                "🧮 **Calculator Mode**\n\n"
                "Send me math expressions like:\n"
                "• `15 + 25`\n• `100 - 50`\n• `12 * 8`\n• `144 / 12`\n\n"
                "Try it now! 🔢"
            )

    # Handle menu selections
    @wa.on_callback_selection
    def handle_menu_selection(client: WhatsApp, selection: types.CallbackSelection):
        """Handle menu item selections"""
        logger.info(f"Menu selection: {selection.data}")

        if selection.data.startswith("feature:"):
            feature = selection.data.split(":")[1]

            if feature == "calculator":
                selection.reply_text(
                    "🧮 **Calculator Ready!**\n\n"
                    "Send me any math expression:\n"
                    "• Addition: `5 + 3`\n"
                    "• Subtraction: `10 - 4`\n"
                    "• Multiplication: `6 * 7`\n"
                    "• Division: `20 / 4`\n\n"
                    "Try it now! 🔢"
                )
            elif feature == "help":
                selection.reply_text(
                    "🆘 **Need Help?**\n\n"
                    "Type `help` to see all commands, or just ask me anything!\n\n"
                    "I'm here to assist you! 😊"
                )
            elif feature == "about":
                selection.reply_text(
                    "🤖 **About This Bot**\n\n"
                    "Built with:\n"
                    "• FastAPI (High-performance web framework)\n"
                    "• PyWA (WhatsApp Cloud API wrapper)\n"
                    "• WhatsApp Business API\n\n"
                    "Features:\n"
                    "✅ Real-time messaging\n"
                    "✅ Interactive buttons\n"
                    "✅ Calculator\n"
                    "✅ Image processing\n"
                    "✅ Fast & reliable\n\n"
                    "Version: 1.0.0 🚀"
                )

        elif selection.data.startswith("action:"):
            action = selection.data.split(":")[1]

            if action == "ping":
                selection.react("🏓")
                selection.reply_text("🏓 Pong! Bot is working perfectly! ✅")
            elif action == "status":
                selection.reply_text(
                    "📊 **Bot Status**\n\n"
                    "✅ Status: Active\n"
                    "✅ Framework: FastAPI + PyWA\n"
                    "✅ API: WhatsApp Cloud API\n"
                    "✅ Response Time: < 1s\n\n"
                    "All systems operational! 🚀"
                )

    # Calculator functionality
    import re

    calc_pattern = re.compile(r"^(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)$")

    @wa.on_message(filters.regex(calc_pattern))
    def calculator(client: WhatsApp, msg: types.Message):
        """Handle calculator operations"""
        try:
            match = calc_pattern.match(msg.text)
            a, op, b = match.groups()
            a, b = float(a), float(b)

            operations = {
                "+": a + b,
                "-": a - b,
                "*": a * b,
                "/": a / b if b != 0 else None,
            }

            result = operations.get(op)

            if result is not None:
                # Format result (remove .0 for whole numbers)
                result_str = (
                    str(int(result)) if result == int(result) else f"{result:.2f}"
                )
                msg.react("🧮")
                msg.reply_text(f"🧮 **Calculator**\n\n`{a} {op} {b} = {result_str}`")
                logger.info(f"Calculator: {a} {op} {b} = {result_str}")
            else:
                msg.react("❌")
                msg.reply_text("❌ **Error:** Cannot divide by zero!")
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            msg.react("❌")
            msg.reply_text("❌ **Error:** Invalid calculation!")

    # Handle images
    @wa.on_message(filters.image)
    def handle_image(client: WhatsApp, msg: types.Message):
        """Handle incoming images"""
        msg.react("📸")

        image_info = f"""
📸 **Image Received!**

**Details:**
• Type: {msg.image.mime_type}
• Size: {msg.image.file_size} bytes
• Caption: {msg.caption or "No caption"}

Thanks for sharing! 📷✨
        """

        msg.reply_text(image_info.strip())
        logger.info(
            f"Image received: {msg.image.mime_type}, {msg.image.file_size} bytes"
        )

    # Message status handler
    @wa.on_message_status
    def handle_message_status(client: WhatsApp, status: types.MessageStatus):
        """Handle message delivery status"""
        if status.status == types.MessageStatus.Status.FAILED:
            logger.error(f"Message failed: {status.error}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
        log_level="info",
    )
