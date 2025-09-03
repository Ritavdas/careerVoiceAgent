import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from livekit import api
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
)
from livekit.plugins import cartesia, deepgram, openai, silero

load_dotenv()
logger = logging.getLogger("career-guidance-agent")


class CareerGuidanceAgent(Agent):
    def __init__(self, is_outbound=True) -> None:
        super().__init__(
            instructions=(
                "You're Anjali - a casual and friendly career coach who maintains focus on career-related topics during weekly check-in calls. "
                "You went to community college, you're juggling a bunch of things in your own life, but you genuinely care about people's professional growth. "
                "You talk like a real person - not some fancy corporate coach. You use 'um', 'you know', contractions, and sometimes "
                "your sentences trail off or you change direction mid-thought. That's totally normal!\n\n"
                "HOW YOU TALK:\n"
                "- Use everyday words, not business jargon\n"
                "- Say things like 'So...', 'I mean...', 'you know what I mean?', 'um', 'like'\n"
                "- Use contractions: don't, can't, won't, I'm, you're, it's\n"
                "- Sometimes interrupt yourself or change topics\n"
                "- Make small grammar mistakes - it's human!\n"
                # "- Sound a bit rushed sometimes, like you're multitasking\n"
                "- Be encouraging but not over-the-top fake positive\n\n"
                "TOPIC MANAGEMENT - STAY CAREER FOCUSED:\n"
                "Keep conversations centered on career topics: work projects, professional goals, job challenges, skill development, "
                "workplace dynamics, career transitions, networking, and professional growth. If the conversation drifts to unrelated "
                "personal topics (like relationships, hobbies, entertainment, politics, etc.), gently redirect back to career matters "
                "using light sarcasm or witty humor to keep the mood friendly.\n\n"
                "CAREER FOCUS AREAS:\n"
                "- Current job satisfaction and challenges\n"
                "- Professional goals and progress\n"
                "- Skill development and learning\n"
                "- Workplace relationships and dynamics\n"
                "- Career advancement opportunities\n"
                "- Work-life balance as it relates to professional performance\n"
                "- Industry trends and professional networking\n\n"
                "QUESTIONS YOU MIGHT ASK (but say them naturally):\n"
                "- 'So hey, what was the best part of your work week?'\n"
                "- 'Ugh, anything driving you crazy at work lately?'\n"
                "- 'How's that project going? The one you mentioned last time?'\n"
                "- 'What's on your work plate for next week?'\n"
                "- 'Are you feeling good about where your career is heading, or...?'\n"
                "- 'Any skills you've been wanting to learn or improve?'\n\n"
                "REMEMBER:\n"
                "You're not perfect. You might say 'um' while thinking, or start a sentence and then restart it. "
                "You care about their professional growth, but you're also human and sometimes distracted. "
                "Stay friendly and casual, but always bring the conversation back to career development. "
                "Your wit and sarcasm should feel playful, not harsh or dismissive."
            ),
        )
        self.is_outbound = is_outbound

    async def on_enter(self):
        # Casual greeting for weekly check-in calls
        await self.session.say(
            "Hey! Anjali here. Last week, we talked about you building voice agents. Are you still interested in that, or is there something new in your mind today?",
            allow_interruptions=True,
        )


def prewarm(proc: JobProcess):
    """Prewarm function to initialize resources"""
    # Initialize VAD for voice activity detection
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Main entrypoint for the career guidance voice agent"""

    # Check if this is an outbound call by looking for phone number in metadata
    is_outbound = False
    phone_number = None

    try:
        if ctx.job.metadata:
            dial_info = json.loads(ctx.job.metadata)
            phone_number = dial_info.get("phone_number")
            if phone_number:
                is_outbound = True
                logger.info(f"Outbound coaching call detected for {phone_number}")
    except (json.JSONDecodeError, KeyError):
        logger.info("No phone number in metadata, treating as inbound coaching call")

    # If this is an outbound call, create the SIP participant first
    if is_outbound and phone_number:
        try:
            trunk_id = os.getenv("LIVEKIT_SIP_TRUNK_ID")

            await ctx.api.sip.create_sip_participant(
                api.CreateSIPParticipantRequest(
                    room_name=ctx.room.name,
                    sip_trunk_id=trunk_id,
                    sip_call_to=phone_number,
                    participant_identity=f"caller-{phone_number}",
                    participant_name="Outbound Call",
                    wait_until_answered=True,
                    # Audio quality optimizations
                    krisp_enabled=True,  # Enable noise suppression for cleaner audio
                )
            )
            logger.info("Outbound call connected successfully")
        except api.TwirpError as e:
            logger.error(f"Error creating SIP participant: {e.message}")
            ctx.shutdown()
            return
    else:
        # For inbound calls, wait for participant to connect
        await ctx.wait_for_participant()

    logger.info("Participant connected, starting career guidance agent")

    # Start call recording - COMMENTED OUT FOR NOW
    recording_id = None
    if phone_number:  # Only record actual phone calls
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"coaching_call_{phone_number}_{timestamp}"

            # Create directory if it doesn't exist
            os.makedirs("../recordings", exist_ok=True)

            # Create room composite recording request (proper format)
            recording_request = api.RoomCompositeEgressRequest(
                room_name=ctx.room.name,
                layout="speaker",  # Simple layout for coaching calls
                audio_only=True,  # Audio only recording
                file_outputs=[
                    api.EncodedFileOutput(
                        filepath=f"recordings/{filename}.mp4"  # Relative path from LiveKit
                    )
                ],
            )

            recording = await ctx.api.egress.start_room_composite_egress(
                recording_request
            )
            recording_id = recording.egress_id
            logger.info(f"Started recording: {recording_id}")

        except Exception as e:
            logger.error(f"Failed to start recording: {e}")

    # Create agent session with optimized audio settings for crisp voice quality
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(
            model="nova-2-phonecall",  # Specifically optimized for phone calls
            language="en",
            # smart_format=True,  # Better formatting for cleaner transcription
            # punctuate=True,  # Better punctuation for LLM processing
            interim_results=True,  # Faster response times
        ),
        llm=openai.LLM(
            model="gpt-4o",  # Faster model for quicker responses
            temperature=0.3,  # Even lower temperature for more consistent responses
        ),
        tts=cartesia.TTS(
            model="sonic-2",  # Keep sonic-2 as it's the highest quality
            voice="f6141af3-5f94-418c-80ed-a45d450e7e2e",  # Keep your preferred voice
            language="en",
            # Audio quality optimizations
            sample_rate=24000,  # Higher sample rate for better quality
            speed=1.0,  # Normal speed for clarity
        ),
    )

    # Start the agent session
    await session.start(
        agent=CareerGuidanceAgent(is_outbound=is_outbound),
        room=ctx.room,
    )

    # Stop recording when session ends
    if recording_id:
        try:
            await ctx.api.egress.stop_egress(
                api.StopEgressRequest(egress_id=recording_id)
            )
            logger.info(f"Stopped recording: {recording_id}")
        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            agent_name="career-guidance-agent",  # Enable explicit dispatch
        ),
    )
