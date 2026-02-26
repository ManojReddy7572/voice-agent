\## Setup Instructions



\### Prerequisites

\- Python 3.10+

\- Git

\- LiveKit Cloud account (Free tier)

\- OpenAI API key



---



\### 1. Clone the Repository



git clone https://github.com/ManojReddy7572/voice-agent.git  

cd voice-agent  



---



\### 2. Create Virtual Environment (Windows)



python -m venv venv  

venv\\Scripts\\activate  



If PowerShell blocks activation, run:



Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process  



Then activate again.



---



\### 3. Install Dependencies



pip install -r requirements.txt  



---



\### 4. Create Environment Variables



Create a file named `.env` in the project root folder.



Add the following:



LIVEKIT\_URL=wss://your-project.livekit.cloud  

LIVEKIT\_API\_KEY=your\_livekit\_api\_key  

LIVEKIT\_API\_SECRET=your\_livekit\_api\_secret  

OPENAI\_API\_KEY=your\_openai\_api\_key  



Replace the values with your actual credentials.



---



\### 5. Run the Voice Agent



python main.py  



---



\### 6. Test the Agent



1\. Open https://meet.livekit.io  

2\. Click \*\*Custom\*\*  

3\. Paste your LIVEKIT\_URL  

4\. Generate a JWT token using the project script  

5\. Paste token and connect  

6\. Speak into microphone  



The agent will respond with:



"You said: <your speech>"



If no speech is detected for 20 seconds, the agent says:



"Are you still there?"



