# 🎯 AI Career Coach Voice Agent

[![LiveKit](https://img.shields.io/badge/LiveKit-Agents-blue)](https://livekit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green)](https://openai.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow)](https://python.org/)
[![Twilio](https://img.shields.io/badge/Twilio-SIP-red)](https://twilio.com/)

## 🎬 Demo

> **Coming Soon!** We're preparing a comprehensive video demonstration showing Anjali in action.

**What the demo will showcase:**

- 📞 **Live outbound call** - See how Anjali initiates and manages calls
- 🗣️ **Natural conversation flow** - Experience realistic career coaching dialogue
- 🎯 **Topic management** - Watch how Anjali keeps conversations career-focused
- 💡 **Personalized advice** - See contextual career guidance in real-time
- 🔊 **Audio quality** - Hear crystal-clear voice synthesis and recognition
A sophisticated AI-powered career coaching voice agent that conducts weekly check-in calls to help professionals grow their careers. Built with LiveKit Agents, this system provides personalized career guidance through natural voice conversations.

## 🌟 Project Overview

**Anjali** is your AI career coach - a casual, friendly, and focused professional development companion who calls you weekly to:

- **Track your professional progress** and career goals
- **Provide personalized career advice** based on your updates
- **Help you navigate workplace challenges** and opportunities
- **Keep conversations focused** on career-related topics
- **Offer actionable insights** for professional growth

Unlike traditional coaching apps, Anjali conducts real voice conversations that feel natural and engaging, making career development more accessible and consistent.

## ✨ Key Features

### 🔊 **Advanced Voice Technology**

- **Outbound SIP calling** via LiveKit/Twilio integration
- **Crystal-clear audio quality** with optimized settings (24kHz sample rate)
- **Real-time conversation** with minimal latency
- **Noise suppression** (Krisp) for professional call quality

### 🤖 **AI-Powered Coaching**

- **Personality-driven conversations** with Anjali, your casual career coach
- **Career topic management** with gentle redirection from off-topic discussions
- **Context-aware responses** that remember previous conversations
- **Natural speech patterns** with human-like imperfections

### 📞 **Professional Call Management**

- **Automated outbound calling** to your phone number
- **Flexible scheduling** for weekly check-ins
- **International phone number support**

### 🎯 **Career-Focused Conversations**

- Work projects and professional challenges
- Skill development and learning opportunities
- Career advancement and goal setting
- Workplace dynamics and networking
- Industry trends and professional growth

## 🎭 Meet Anjali: Your AI Career Coach

Anjali is designed to feel like a real person - not a corporate coaching bot. Here's what makes Anjali special:

### Personality Traits

- **Community college educated** - relatable and down-to-earth
- **Casual communication style** - uses "um", "you know", contractions
- **Slightly imperfect speech** - sometimes trails off or restarts sentences
- **Genuinely caring** but not overly polished or fake-positive
- **Focused on results** - keeps conversations on career topics

### Coaching Approach

- **Weekly check-ins** to track your professional progress
- **Active listening** with thoughtful follow-up questions
- **Gentle redirection** when conversations drift off-topic
- **Practical advice** based on your specific situation
- **Encouraging but realistic** feedback and suggestions

### Sample Questions Anjali Asks

- "So hey, what was the best part of your work week?"
- "Ugh, anything driving you crazy at work lately?"
- "Are you feeling good about where your career is heading, or...?"
- "Any skills you've been wanting to learn or improve?"

## 🛠 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Agent Framework** | LiveKit Agents | Real-time voice agent orchestration |
| **Large Language Model** | OpenAI GPT-4o-mini | Conversation intelligence and responses |
| **Text-to-Speech** | Cartesia Sonic-2 | High-quality voice synthesis |
| **Speech-to-Text** | Deepgram Nova-2-phonecall | Phone-optimized transcription |
| **SIP Integration** | Twilio | Outbound calling infrastructure |
| **Voice Processing** | Silero VAD | Voice activity detection |

### 🎮 Try It Yourself

Want to experience Anjali right now? Here's what a typical call looks like:

1. **You receive a call** from your configured Twilio number
2. **Anjali greets you** with context from your last conversation
3. **Natural conversation** about your work week and challenges
4. **Career-focused guidance** with actionable advice
5. **Call ends** with clear next steps and encouragement

**Total call time**: Usually 5-15 minutes, depending on what you want to discuss.

### 🎯 Demo Scenarios

**Scenario 1: Weekly Check-in**

```
Anjali: "Hey! It's Anjali. How's your week been going work-wise?"
You: "Pretty good, but I'm feeling stuck on this project..."
Anjali: "Ugh, that's frustrating. What's making you feel stuck exactly?"
```

**Scenario 2: Career Planning**

```
Anjali: "So, where do you see yourself career-wise in the next year?"
You: "I want to move into a leadership role..."
Anjali: "Nice! What skills do you think you need to work on for that?"
```

**Scenario 3: Topic Redirection**

```
You: "I've been binge-watching this new series..."
Anjali: "That's cool, but let's focus on your career stuff. Any wins at work this week?"
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - Programming language runtime
- **LiveKit Cloud account** - Real-time communication platform ([Sign up](https://livekit.io/))
- **OpenAI API access** - For GPT-4 conversation intelligence ([Get API key](https://platform.openai.com/))
- **Deepgram API access** - For speech-to-text transcription ([Get API key](https://deepgram.com/))
- **Twilio account with SIP trunk** - For outbound calling ([Setup guide](https://www.twilio.com/docs/sip-trunking))
- **Cartesia API access** - For high-quality text-to-speech ([Get API key](https://cartesia.ai/))

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd careerVoiceAgent
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your API credentials
```

4. **Configure your environment**

```bash
# Required API keys and configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
LIVEKIT_SIP_TRUNK_ID=your_sip_trunk_id

OPENAI_API_KEY=your_openai_key
DEEPGRAM_API_KEY=your_deepgram_key
CARTESIA_API_KEY=your_cartesia_key

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

### Usage

#### Start the Career Coach Agent

```bash
python career_coach.py dev
```

#### Make an Outbound Coaching Call

```bash
python make_outbound_call.py +1234567890
```

#### Example Output

```
📞 Making outbound coaching call to +1234567890
🏠 Room: coaching-1234567890
==================================================
✅ Career coach dispatch created: dispatch_abc123
🎯 Coach should now be calling +1234567890
📊 Monitor at: https://your-project.livekit.cloud/rooms/coaching-1234567890
```

## ⚙️ Configuration

### Audio Quality Settings

The agent is optimized for crystal-clear voice quality:

```python
# High-quality TTS settings
tts=cartesia.TTS(
    model="sonic-2",
    sample_rate=24000,  # High-quality audio
    speed=1.0,          # Natural speaking pace
)

# Phone-optimized STT
stt=deepgram.STT(
    model="nova-2-phonecall",  # Phone call optimized
    interim_results=True,       # Faster responses
)
```

### Agent Personality Customization

Anjali's personality can be customized in `career_coach.py`:

```python
# Modify the instructions to change Anjali's:
# - Communication style
# - Career focus areas
# - Redirection techniques
# - Question patterns
```

## 📁 Project Structure

```
careerVoiceAgent/
├── career_coach.py          # Main AI agent implementation
├── make_outbound_call.py    # Outbound calling script
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration
├── .env.example            # Environment template
└── README.md              # This file
```

## 💬 Conversation Examples

### Sample Career Coaching Dialogue

**Anjali**: "Hey! Anjali here. Last week, we talked about you building voice agents. Are you still interested in that, or is there something new in your mind today?"

**You**: "Yeah, I'm still working on the voice agent project, but I'm also thinking about learning some new frameworks."

**Anjali**: "Nice! So how's the voice agent stuff going? Any roadblocks you're hitting, or is it flowing pretty well?"

**You**: "It's going okay, but I'm struggling with the audio quality optimization."

**Anjali**: "Ugh, audio stuff can be tricky. What specifically is bugging you about it? Like, is it the clarity, or latency, or...?"

### Topic Redirection Examples

**You**: "Oh, and I watched this amazing Netflix series last weekend..."

**Anjali**: "That's cool and all, but I'm here to talk about your career, not your Netflix habits! So back to that audio optimization - what have you tried so far?"

**You**: "I've been having some relationship drama lately..."

**Anjali**: "I mean, that's tough, but are we gonna talk about your professional life or what? How's work treating you this week?"

## 🔧 Troubleshooting

### Common Issues

**Call Quality Issues**

- Ensure stable internet connection
- Check Twilio SIP trunk configuration
- Verify phone number format (+1234567890)

**Agent Not Responding**

- Verify all API keys are correct
- Check LiveKit agent deployment status
- Monitor logs for error messages

**Connection Failures**

- Confirm SIP trunk ID is correct
- Verify Twilio account permissions
- Check phone number verification status

### Debug Mode

Enable detailed logging:

```bash
export LIVEKIT_LOG_LEVEL=debug
python career_coach.py dev
```

### Support

For technical issues:

1. Check the [LiveKit Documentation](https://docs.livekit.io/)
2. Review API provider status pages
3. Verify environment configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [LiveKit](https://livekit.io/) for the real-time communication platform
- [OpenAI](https://openai.com/) for the conversational AI capabilities
- [Cartesia](https://cartesia.ai/) for high-quality text-to-speech
- [Deepgram](https://deepgram.com/) for accurate speech recognition
- [Twilio](https://twilio.com/) for reliable SIP infrastructure
