# 🚀 Quick Start Guide - Career Coach WhatsApp Bot

## ⚡ **EVERY TIME STARTUP - 6 STEPS**

### **1. Rotate Access Token**

```bash
1. Go to developers.facebook.com
2. Your App → WhatsApp → API Setup
3. Generate new Access Token
4. Update .env: ACCESS_TOKEN=new_token_here
```

### **2. Start Cloudflare Tunnel**

```bash
# Your Cloudflare tunnel command
# Note the new URL: https://random-words.trycloudflare.com
```

### **3. Update .env**

```env
CALLBACK_URL=https://your-new-cloudflare-url.trycloudflare.com
ACCESS_TOKEN=your_new_access_token
```

### **4. Start Server**

```bash
python career_coach_webhook.py
# Wait for: "✅ Career Coach bot initialized (send-only mode)"
```

### **5. Register Webhook**

```bash
curl -X POST http://localhost:3000/register-webhook
# Wait for: "status": "success"
```

### **6. Test Bot**

```
Send WhatsApp message: "hello" or "test"
```

---

## 🔧 **Debug Commands**

```bash
# Check status
curl http://localhost:3000/webhook-test
curl http://localhost:3000/health

# Test manual message
curl -X POST http://localhost:3000/send-message \
  -H "Content-Type: application/json" \
  -d '{"to":"YOUR_PHONE","message":"Test"}'
```

---

## ❌ **If Something Breaks**

1. **401 Unauthorized** → Wrong APP_SECRET in .env
2. **No response to messages** → Redo webhook registration
3. **Server won't start** → Check .env file format
4. **Webhook fails** → Verify Cloudflare URL is accessible

---

## 📋 **Success Checklist**

- ✅ New access token from Meta
- ✅ Cloudflare tunnel running  
- ✅ .env file updated
- ✅ Server started successfully
- ✅ Webhook registered (200 response)
- ✅ Bot replies to test messages

**Full details**: See [SETUP_INSTRUCTIONS.md](./SETUP_INSTRUCTIONS.md)
