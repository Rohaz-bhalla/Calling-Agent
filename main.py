import asyncio
import traceback
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext, RoomOptions, WorkerJob, Options
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from dotenv import load_dotenv
import os
import logging

# Set logging to INFO to see the agent join the room
logging.basicConfig(level=logging.INFO)

load_dotenv()

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful AI assistant that answers phone calls. Keep your responses concise and friendly.",
        )

    async def on_enter(self) -> None:
        # This triggers as soon as the AI joins the call
        await self.session.say("Hello! I'm your real-time assistant. How can I help you today?")

    async def on_exit(self) -> None:
        await self.session.say("Goodbye! It was great talking with you![cite: 1]")

async def start_session(context: JobContext):
    # Configure Gemini with the API Key from your .env
    model = GeminiRealtime(
        model="gemini-1.5-flash-8b", # Use a stable model name
        api_key=os.getenv("GOOGLE_API_KEY"),
        config=GeminiLiveConfig(
            voice="Leda",
            response_modalities=["AUDIO"]
        )
    )
    
    pipeline = Pipeline(llm=model)
    # Pass the session to the context so the worker knows it's active
    session = AgentSession(agent=MyVoiceAgent(), pipeline=pipeline)

    print(f"🚀 Agent is joining Room: {context.room_id}")
    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:
    room_options = RoomOptions()
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    try:
        # We removed 'idle_processes' because your version of the SDK doesn't support it.
        # Keeping max_processes=1 is the most important part for your laptop's performance.
        options = Options(
            agent_id="MyTelephonyAgent", 
            register=True,               
            max_processes=1,             
            host="0.0.0.0", 
            port=8081,
        )
        
        job = WorkerJob(entrypoint=start_session, jobctx=make_context, options=options)
        
        print("🤖 AI Worker is starting... (Lean mode)")
        job.start()
        
    except Exception as e:
        print("❌ Worker failed to start:")
        traceback.print_exc()