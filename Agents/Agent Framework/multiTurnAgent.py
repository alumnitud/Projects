import os
import asyncio

from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

async def main():
    credential = AzureCliCredential()
    client = AzureOpenAIResponsesClient(
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        deployment_name= os.getenv("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"),
        credential=credential, 
        )
    
    agent= client.as_agent(
        name= "PersonalBuddy",
        instructions= "You are a helpful assistant. Keep your responses brief.",
    )

    # To maintain conversation history
    session= agent.create_session()

    # multi-turn conversation with session management
    result= await agent.run("My name is Alice. I like hiking and painting.", session=session)
    print(f"Agent: {result}\n")

    result= await agent.run("What do you know about me?", session=session)
    print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 