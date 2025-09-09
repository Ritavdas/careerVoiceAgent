# 🤖 WhatsApp Bot - FastAPI + PyWA

A simple yet powerful WhatsApp bot built with **FastAPI** and **PyWA** for the WhatsApp Cloud API.

## 🚀 Features

- ✅ **Interactive Messaging** - Buttons, menus, and rich interactions
- 🧮 **Built-in Calculator** - Perform math calculations
- 📸 **Image Processing** - Handle and respond to images
- 🏓 **Health Monitoring** - API endpoints for bot status
- 📊 **Auto Documentation** - Swagger UI at `/docs`
- ⚡ **High Performance** - FastAPI async capabilities
- 🔒 **Type Safe** - Full TypeScript-like safety in Python

## 📋 Prerequisites

1. **Meta Developer Account** - [developers.facebook.com](https://developers.facebook.com/)
2. **WhatsApp Business Account** - Verified business account
3. **Python 3.9+** - Required for PyWA
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

4. **Run the bot:**
   ```bash
   # Development mode
   fastapi dev main.py --port 8000
   
   # Or production mode
   uvicorn main:app --host 0.0.0.0 --port 8000
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

### 📍 How to Get These Values:

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

## 🎮 Bot Commands

Once running, your bot supports:

### 💬 **Text Commands**
- `hi/hello/hey` - Welcome message with interactive buttons
- `help` - Show help and available commands
- `ping` - Test bot response (replies with "Pong!")
- `menu` - Show interactive menu options

### 🧮 **Calculator**
Send math expressions:
- `15 + 25` → `40`
- `100 - 50` → `50`
- `12 * 8` → `96`
- `144 / 12` → `12`

### 🖼️ **Media**
- Send images → Bot provides image details
- Support for various file types

### 🎯 **Interactive Features**
- **Buttons** - Quick action buttons
- **Lists** - Organized menu selections
- **Reactions** - Emoji reactions to messages

## 📊 API Endpoints

Your bot also provides HTTP API endpoints:

- `GET /` - Bot status and info
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `POST /send-message` - Send message to specific number
- `POST /broadcast` - Send message to multiple recipients

### Example API Usage:
```bash
# Send a message
curl -X POST "http://localhost:8000/send-message" \\
     -H "Content-Type: application/json" \\
     -d '{
       "to": "+919650098052",
       "message": "Hello from API!"
     }'
```

## 🚀 Deployment

### **Railway (Recommended)**
1. Fork/upload your code to GitHub
2. Connect to [Railway](https://railway.app/)
3. Add environment variables
4. Deploy automatically

### **Heroku**
```bash
# Install Heroku CLI, then:
heroku create your-bot-name
heroku config:set PHONE_ID=your_phone_id
heroku config:set ACCESS_TOKEN=your_token
# ... add other env vars
git push heroku main
```

### **Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Development

### **Project Structure**
```
whatsapp_bot/
├── main.py              # Main application
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
├── .env               # Your actual environment (don't commit!)
├── README.md          # This file
└── .gitignore         # Git ignore patterns
```

### **Adding New Features**
```python
# Add to main.py

@wa.on_message(filters.text & filters.startswith('custom'))
def custom_handler(client: WhatsApp, msg: types.Message):
    msg.reply_text("Custom feature activated!")
```

### **Testing**
```bash
# Run tests (if you add pytest)
pytest

# Test specific functionality
python -c "import main; print('Bot loaded successfully!')"
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

- **PyWA Documentation:** [pywa.readthedocs.io](https://pywa.readthedocs.io/)
- **WhatsApp Cloud API Docs:** [developers.facebook.com/docs/whatsapp](https://developers.facebook.com/docs/whatsapp)
- **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

## 📄 License

This project is open source and available under the MIT License.

---

🎉 **Happy Bot Building!** 🤖

Built with ❤️ using FastAPI + PyWA