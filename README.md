\# 🎙️ Real-Time Voice Agent (LiveKit)



\## Overview

This project implements a real-time voice agent using LiveKit Cloud.



The agent:

\- Joins a LiveKit room

\- Listens to user audio

\- Converts speech to text (STT)

\- Responds with: "You said: <text>"

\- Converts response to speech (TTS)

\- Publishes audio back to the room



\## Features Implemented



\### ✅ STT → TTS Pipeline

User Speech → Whisper (STT) → Generate response → OpenAI TTS → Publish audio



\### ✅ No Overlap Handling

\- Agent maintains LISTENING and SPEAKING states

\- If user speaks while agent is speaking, agent stops immediately

\- Implemented using energy-based detection and explicit state logic



\### ✅ Silence Handling

\- If no user speech for 20+ seconds

\- Agent says: "Are you still there?"

\- Prevents continuous publishing



\## Architecture



User Audio  

↓  

Energy Detection (RMS-based VAD)  

↓  

Buffer Audio  

↓  

OpenAI Whisper (STT)  

↓  

Generate Response  

↓  

OpenAI TTS  

↓  

Publish Audio via LiveKit  



\## Setup Instructions



\### 1. Clone repository

