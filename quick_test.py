import asyncio
import os
from webact.agent import WebActAgent

# Setup your API Key here, or pass through environment
# os.environ["OPENAI_API_KEY"] = "Your API KEY Here"
os.environ["GEMINI_API_KEY"] ="your_googleapi_key"  

async def run_agent():
    agent = WebActAgent(model="gemini-2.0-flash-exp", default_task="Find the price of iPhone 15", default_website="https://www.apple.com/")
    await agent.start()
    while not agent.complete_flag:
        prediction_dict = await agent.predict()
        await agent.execute(prediction_dict)
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(run_agent())
