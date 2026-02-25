async def on_audio_frame(frame):
    if vad.is_speech(frame):
        agent.update_speech_timestamp()

        if agent.state == "SPEAKING":
            await agent.stop_speaking()

        agent.buffer.append(frame)