# 🤖 WhatsApp Career Coach Bot - Direct API

A powerful WhatsApp bot built with **FastAPI** and **Direct WhatsApp Cloud API** calls for career coaching and advice.

## 🚀 Features

- ✅ **Career Coaching** - Specialized advice for career development
- 🎯 **Interactive Buttons** - Quick access to resume tips, interview prep, salary negotiation
- 💼 **Smart Keyword Detection** - Automatically responds to career-related queries
- 📱 **Two-Way Communication** - Full conversational WhatsApp bot
- 🏓 **Health Monitoring** - API endpoints for bot status
- 📊 **Auto Documentation** - Swagger UI at `/docs`
- ⚡ **High Performance** - FastAPI async capabilities
- 🔒 **Direct API Integration** - No third-party libraries, full control

## 📋 Prerequisites

1. **Meta Developer Account** - [developers.facebook.com](https://developers.facebook.com/)
2. **WhatsApp Business Account** - Verified business account
3. **Python 3.9+** - For FastAPI and direct API calls
4. **Public URL** - For webhooks (use ngrok for testing)

## 🛠️ Installation

1. **Clone/Navigate to the bot directory:**

   ```bash
   cd whatsapp_bot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **⚠️ IMPORTANT: Complete Setup Instructions:**

   **📋 See [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md) for the complete step-by-step guide!**

   This includes the required workflow for:
   - 🔄 Rotating access tokens (required every time)
   - 🌐 Starting Cloudflare tunnels
   - 🔗 Webhook registration process
   - 🐛 Troubleshooting common issues

5. **Quick Start (after reading setup instructions):**

    ```bash
    # Start the server
    python whatsapp_direct_api.py
    ```

## ⚙️ Environment Variables

You need to provide these environment variables in your `.env` file:

### 🔑 Required Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `PHONE_ID` | WhatsApp Business phone number ID | Meta Developer Console → App → WhatsApp → API Setup |
| `ACCESS_TOKEN` | Permanent access token | Meta Developer Console → App → WhatsApp → API Setup |
| `APP_ID` | Meta app ID | Meta Developer Console → App → Settings → Basic |
| `APP_SECRET` | Meta app secret | Meta Developer Console → App → Settings → Basic |
| `CALLBACK_URL` | Your public webhook URL | Your domain or ngrok URL |
| `VERIFY_TOKEN` | Custom webhook verification token | Choose any secure string |

### 📍 How to Get These Values

#### 1. **PHONE_ID & ACCESS_TOKEN**

- Go to [Meta Developer Console](https://developers.facebook.com/)
- Select your app → **WhatsApp** → **API Setup**  
- Copy **Phone Number ID** and **Access Token**

#### 2. **APP_ID & APP_SECRET**

- In Meta Developer Console → Your App → **Settings** → **Basic**
- Copy **App ID** and **App Secret**

#### 3. **CALLBACK_URL**

- Your public domain: `https://yourdomain.com`
- For testing with ngrok: `https://abc123.ngrok.io`

#### 4. **VERIFY_TOKEN**

- Create any secure string (e.g., `my_secure_token_123`)
- You'll use this when setting up webhooks

## 🌐 Webhook Setup

1. **Get a public URL:**

   ```bash
   # For testing - install ngrok
   ngrok http 8000
   # Copy the https URL (e.g., https://abc123.ngrok.io)
   ```

2. **Configure webhook in Meta Console:**
   - Go to **WhatsApp** → **Configuration** → **Webhook**
   - **Callback URL:** `https://your-url.com` (or ngrok URL)
   - **Verify Token:** Same as in your `.env` file
   - **Webhook fields:** Check `messages`

3. **Test webhook:**
   - Meta will send a verification request
   - Your bot should respond correctly if configured properly

## 🎮 Career Coach Commands

Once running, your bot provides career coaching:

### 💬 **Career Keywords**

- `hi/hello/hey/start` - Welcome message with career coaching buttons
- `resume` - Get detailed resume writing tips
- `interview` - Interview preparation advice
- `salary/negotiation` - Salary negotiation strategies
- `job/career/work/skills/promotion` - General career advice

### 🎯 **Interactive Buttons**

- **🎯 Career Goals** - Set and plan your career objectives
- **📝 Resume Tips** - Professional resume optimization
- **🔍 Job Search** - Effective job hunting strategies

### 🧪 **Testing**

- `test/ping/webhook` - Test webhook connectivity
- Send any career-related message for personalized advice

### 💼 **Career Coaching Features**

- **Smart Detection** - Automatically identifies career-related queries
- **Personalized Responses** - Tailored advice based on your questions
- **Interactive Menus** - Easy navigation through career topics
- **Professional Guidance** - Expert career development tips

## 📊 API Endpoints

Your bot provides these HTTP API endpoints:

- `GET /` - Bot status and environment info
- `GET /health` - Health check with readiness status
- `GET /docs` - Interactive API documentation (Swagger UI)
- `POST /send-message` - Send message to specific WhatsApp number
- `GET /test-webhook` - Test webhook configuration and get setup instructions

### Example API Usage

```bash
# Send a message
curl -X POST "http://localhost:8000/send-message" \\
      -H "Content-Type: application/json" \\
      -d '{
        "to": "+919650098052",
        "message": "Hello from API!"
      }'

# Check webhook configuration
curl http://localhost:8000/test-webhook
```

## 🔧 Development

### **Project Structure**

```
whatsapp_bot/
├── whatsapp_direct_api.py    # Main application (Direct WhatsApp API)
├── career_coach_webhook.py   # Previous PyWA implementation
├── main_simple.py           # Simple send-only version
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── .env                    # Your actual environment (don't commit!)
├── README.md               # This file
├── logs.md                 # Project journey and decisions
└── .gitignore             # Git ignore patterns
```

### **Adding New Features**

```python
# Add to whatsapp_direct_api.py

# Add new career advice topics
CAREER_ADVICE["new_topic"] = """Your new career advice here..."""

# Add new keyword handlers in handle_text_message()
elif "new_keyword" in text_lower:
    if phone_number_id:
        await send_text_message(sender, CAREER_ADVICE["new_topic"], phone_number_id)
```

## ❓ Troubleshooting

### **Common Issues:**

1. **"WhatsApp client not initialized"**
   - Check your environment variables
   - Ensure all required fields are filled
   - Verify tokens are correct

2. **Webhook verification failed**
   - Make sure `VERIFY_TOKEN` matches in both .env and Meta Console
   - Check that your webhook URL is accessible
   - Ensure ngrok is running (if using for testing)

3. **Messages not being received**
   - Verify webhook is configured correctly
   - Check webhook fields include "messages"
   - Look at server logs for errors

4. **Import errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Use correct Python version (3.9+)

### **Debug Mode**

```bash
# Run with debug logging
DEBUG=true fastapi dev main.py
```

### **Check Bot Status**

```bash
# Test health endpoint
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

## 🤝 Support

- **WhatsApp Cloud API Docs:** [developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp)
- **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **Direct API Implementation:** No third-party library dependencies

## 📄 License

This project is open source and available under the MIT License.

---

🎉 **Happy Career Coaching!** 🤖

Built with ❤️ using FastAPI + Direct WhatsApp Cloud API
