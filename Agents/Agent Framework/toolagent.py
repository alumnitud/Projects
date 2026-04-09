import os
import asyncio
from random import randint
from typing import Annotated #This is used for adding metadata (like description) to function parameters, which can be useful for tools that need to understand the purpose of each parameter.
from pydantic import Field #This is used to define the structure of the data and add validation. In this code, it's used to provide a description for the 'location' parameter in the get_weather tool.

from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework import tool
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

# <define_tool>
# NOTE: approval_mode="never_require" is for sample brevity.
# Use "always_require" in production for user confirmation before tool execution.
@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."
# </define_tool>

async def main(response_type: str = "sync"):
    credential = AzureCliCredential()
    client = AzureOpenAIResponsesClient(
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        deployment_name= os.getenv("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"),
        credential=credential, 
        )

    # Create the Agent
    agent= client.as_agent(
        name= "LearningBuddy",
        instructions= """You are a helpful weather agent. Use the get_weather tool to answer questions.""",
        tools= get_weather,
    )

    # User can choose between synchronous (non-streaming) or asynchronous (streaming) response generation.

    if response_type == "sync":
        # Generate response (non-streaming- get complete response at once)
        result= await agent.run("What is a the weather in Munich?")
        print(f"Agent: {result}")
    elif response_type == "async":
        # Generate response (streaming)
        # Streaming: receive tokens as they are generated
        print("Agent (streaming): ", end="", flush=True)
        async for chunk in agent.run("What is the weather in New Delhi?", stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()
    else:
        print("Invalid choice. Please enter 'sync' or 'async'.")

if __name__ == "__main__":
    choice = input("Choose response type - sync or async: ").strip().lower()
    asyncio.run(main(response_type=choice))