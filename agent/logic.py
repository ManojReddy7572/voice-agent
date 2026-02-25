async def process_speech():
    text = await stt.transcribe(buffer)
    response = f"You said: {text}"
    audio = await tts.generate(response)
    await publish_audio(audio)