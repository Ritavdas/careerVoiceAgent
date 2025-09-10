# WhatsApp Career Coach Bot - Complete Setup Instructions

## 🔄 **EVERY TIME STARTUP PROCEDURE**

You need to follow these steps **EVERY TIME** you want to run the bot:

### **Step 1: Rotate Access Token** 🔑

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Navigate to: **Your App → WhatsApp → API Setup**
3. Find your **Phone Number ID** section
4. Click **"Generate Access Token"** or **"Refresh Token"**
5. Copy the new access token
6. Update your `.env` file:

   ```bash
   ACCESS_TOKEN=your_new_access_token_here
   ```

### **Step 2: Start Cloudflare Tunnel** 🌐

```bash
# Start your Cloudflare tunnel (this gives you the public URL)
cloudflare-tunnel-command-here
# Note down the URL: https://something-random-words.trycloudflare.com
```

### **Step 3: Update Environment Variables** 📝

Update your `.env` file with the new Cloudflare URL:

```bash
CALLBACK_URL=https://your-new-cloudflare-url.trycloudflare.com
```

### **Step 4: Start the Server** 🚀

```bash
python career_coach_webhook.py
```

Wait for: `✅ Career Coach bot initialized (send-only mode)`

### **Step 5: Register Webhook** 🔗

```bash
curl -X POST http://localhost:3000/register-webhook
```

Wait for: `"status": "success", "webhook_active": true`

### **Step 6: Test the Bot** 💬

Send a WhatsApp message to your bot number:

- Try: `hello`, `test`, `resume`, `interview`

---

## 🔧 **Meta Developer Console Configuration**

### **Webhook Configuration**

- **Callback URL**: Your current Cloudflare URL
- **Verify Token**: `career_coach_webhook_token_2024`
- **Webhook Fields**: ✅ `messages`, ✅ `message_status`, ✅ `messaging_postbacks`

### **Test Recipients**

Add your personal phone number to test recipients in:
**WhatsApp → API Setup → Recipient Phone Numbers**

---

## 🐛 **Troubleshooting Commands**

```bash
# Check webhook status
curl http://localhost:3000/webhook-test

# Check server health
curl http://localhost:3000/health

# Test manual message sending
curl -X POST http://localhost:3000/send-message \
  -H "Content-Type: application/json" \
  -d '{"to":"YOUR_PHONE_NUMBER","message":"Test message"}'

# Check if Cloudflare URL is accessible
curl https://your-cloudflare-url.trycloudflare.com/
```

---

## ⚠️ **Common Issues & Solutions**

### **401 Unauthorized**

- **Problem**: Wrong APP_SECRET
- **Solution**: Copy exact App Secret from Meta Console → Basic Settings

### **422 Unprocessable Content**

- **Problem**: Normal for manual URL access
- **Solution**: This is expected - webhooks work fine

### **Messages Not Processed**

- **Problem**: Handlers not registered
- **Solution**: Make sure `/register-webhook` shows success

### **RuntimeError: Failed to register callback URL**

- **Problem**: Webhook registration timing issue
- **Solution**: Start server first, then call `/register-webhook`

---

## 📋 **Complete Environment Variables Checklist**

Your `.env` file should contain:

```env
# WhatsApp Business API Configuration
PHONE_ID=your_phone_id
ACCESS_TOKEN=your_current_access_token  # ← Update this every time!
BUSINESS_ID=your_business_id

# Meta App Configuration  
APP_ID=your_app_id
APP_SECRET=your_app_secret

# Webhook Configuration
CALLBACK_URL=https://your-current-cloudflare-url.trycloudflare.com  # ← Update this every time!
VERIFY_TOKEN=career_coach_webhook_token_2024

# Server Configuration
PORT=3000
DEBUG=true
```

---

## 🎯 **Success Indicators**

When everything works correctly, you should see:

1. ✅ Server starts without errors
2. ✅ `/register-webhook` returns success
3. ✅ WhatsApp messages show in server logs: `📨 Received from Name: message`
4. ✅ Bot replies to your WhatsApp messages
5. ✅ Interactive buttons work in WhatsApp

---

## 📞 **Emergency Commands**

If bot stops working:

```bash
# 1. Check if server is still running
curl http://localhost:3000/health

# 2. Check webhook status
curl http://localhost:3000/webhook-test

# 3. Restart webhook registration
curl -X POST http://localhost:3000/register-webhook

# 4. If all else fails - restart server and redo setup
```

---

## 🔄 **Why This Process is Needed**

- **Access tokens expire** regularly for security
- **Cloudflare tunnels get new URLs** each time you start them
- **Webhook URLs must match** what's registered with Meta
- **Server must be running** before webhook registration for verification

This setup ensures your bot works reliably every time you start it!
