import os
import asyncio
import numpy as np
import time
import tempfile
from dotenv import load_dotenv
from livekit import rtc
from livekit.api import AccessToken, VideoGrants
from openai import OpenAI
import soundfile as sf

load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ROOM_NAME = "test-room"
BOT_IDENTITY = "voice-bot"

ENERGY_THRESHOLD = 300
SILENCE_SECONDS = 20

agent_state = "LISTENING"
last_user_speech_time = time.time()
audio_buffer = []
client = OpenAI(api_key=OPENAI_API_KEY)


def create_token():
    token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity(BOT_IDENTITY)
    token.with_grants(VideoGrants(room_join=True, room=ROOM_NAME))
    return token.to_jwt()


def calculate_rms(frame):
    samples = np.frombuffer(frame.data, dtype=np.int16)
    return np.sqrt(np.mean(samples ** 2))


async def speak_text(room, text):
    global agent_state
    agent_state = "SPEAKING"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(response.content)
        tts_path = f.name

    data, samplerate = sf.read(tts_path, dtype="int16")
    track = rtc.LocalAudioTrack.create_audio_track("bot-voice")
    source = rtc.AudioSource(samplerate, 1)
    await track.start(source)
    await room.local_participant.publish_track(track)

    chunk = 960
    for i in range(0, len(data), chunk):
        if agent_state != "SPEAKING":
            break
        frame = rtc.AudioFrame(data[i:i+chunk].tobytes(), samplerate, 1, chunk)
        await source.capture_frame(frame)
        await asyncio.sleep(0.02)

    agent_state = "LISTENING"


async def process_audio(room):
    global audio_buffer

    if not audio_buffer:
        return

    audio_np = np.concatenate(audio_buffer)
    audio_buffer = []

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        sf.write(f.name, audio_np, 48000)
        audio_path = f.name

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_path, "rb")
    )

    text = transcript.text
    print("User said:", text)

    reply = f"You said: {text}"
    await speak_text(room, reply)


async def silence_checker(room):
    global last_user_speech_time
    while True:
        await asyncio.sleep(1)
        if time.time() - last_user_speech_time > SILENCE_SECONDS:
            print("Silence reminder")
            await speak_text(room, "Are you still there?")
            last_user_speech_time = time.time()


async def main():
    global agent_state, last_user_speech_time, audio_buffer

    token = create_token()
    room = rtc.Room()

    print("Connecting...")
    await room.connect(LIVEKIT_URL, token)
    print("Connected.")

    asyncio.create_task(silence_checker(room))

    @room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        if track.kind == rtc.TrackKind.KIND_AUDIO:

            async def read_audio():
                global agent_state, last_user_speech_time, audio_buffer

                async for frame in track:
                    energy = calculate_rms(frame)

                    if energy > ENERGY_THRESHOLD:
                        last_user_speech_time = time.time()

                        if agent_state == "SPEAKING":
                            print("Interrupted")
                            agent_state = "LISTENING"

                        samples = np.frombuffer(frame.data, dtype=np.int16)
                        audio_buffer.append(samples)

                    else:
                        if audio_buffer:
                            await process_audio(room)

            asyncio.create_task(read_audio())

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())