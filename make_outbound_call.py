#!/usr/bin/env python3
"""
Script to make outbound coaching calls using LiveKit dispatch
"""

import asyncio
import logging
import os
import random

from dotenv import load_dotenv
from livekit import api

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("outbound-coach")


async def make_outbound_call(phone_number: str):
    """Make an outbound coaching call to the specified phone number"""

    livekit_api = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
    )

    # Generate unique room name
    room_name = f"coaching-{''.join(str(random.randint(0, 9)) for _ in range(10))}"

    print(f"📞 Making outbound coaching call to {phone_number}")
    print(f"🏠 Room: {room_name}")
    print("=" * 50)

    try:
        # Create dispatch request
        response = await livekit_api.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name="career-guidance-agent",
                room=room_name,
                metadata=f'{{"phone_number": "{phone_number}"}}',
            )
        )

        print(f"✅ Career coach dispatch created: {response.dispatch_id}")
        print(f"🎯 Coach should now be calling {phone_number}")
        print(f"📊 Monitor at: {os.getenv('LIVEKIT_URL')}/rooms/{room_name}")

        return response.dispatch_id

    except Exception as e:
        print(f"❌ Failed to create dispatch: {e}")
        return None


async def main():
    """Main function"""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python make_outbound_call.py <phone_number>")
        print("Example: python make_outbound_call.py +919650098052")
        print("This will initiate a weekly coaching check-in call.")
        sys.exit(1)

    phone_number = sys.argv[1]

    # Validate phone number format
    if not phone_number.startswith("+"):
        print("❌ Phone number must be in international format (e.g., +919650098052)")
        sys.exit(1)

    dispatch_id = await make_outbound_call(phone_number)

    if dispatch_id:
        print(f"\n🎉 Coaching call initiated successfully!")
        print(f"📋 Dispatch ID: {dispatch_id}")
        print(f"📞 Your phone should ring shortly for your weekly check-in...")
        print(f"💬 Alex, your career coach, is ready to connect!")
    else:
        print(f"\n💥 Failed to initiate coaching call")


if __name__ == "__main__":
    asyncio.run(main())
