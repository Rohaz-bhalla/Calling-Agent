import asyncio
import traceback
import os
import logging
# Only import the bare essentials at the top
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext, RoomOptions, WorkerJob, Options
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful AI assistant that answers phone calls. Keep your responses concise and friendly.",
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! I'm your real-time assistant. How can I help you today?")

async def start_session(context: JobContext):
    # HEAVY IMPORTS MOVED HERE: These only load when the call actually starts
    from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
    
    model = GeminiRealtime(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("GOOGLE_API_KEY"),
        config=GeminiLiveConfig(
            voice="Leda",
            response_modalities=["AUDIO"]
        )
    )
    
    pipeline = Pipeline(llm=model)
    session = AgentSession(agent=MyVoiceAgent(), pipeline=pipeline)

    print(f"🚀 Agent is joining Room: {context.room_id}")
    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:
    return JobContext(room_options=RoomOptions())

if __name__ == "__main__":
    try:
        # Strictly 1 process, no extra fluff
        options = Options(
            agent_id="MyTelephonyAgent", 
            register=True,               
            max_processes=1,             
            host="0.0.0.0", 
            port=8081,
        )
        
        job = WorkerJob(entrypoint=start_session, jobctx=make_context, options=options)
        
        print("🤖 AI Worker is starting... (Fast-Boot Mode)")
        job.start()
        
    except Exception as e:
        print("❌ Worker failed to start:")
        traceback.print_exc()