import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool
# For search functionality:
from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType
from azure.ai.projects.models import ConnectionType
#for bing grounding tool
from azure.ai.agents.models import BingGroundingTool

# One issue here is that during the creation of the agent, if it runs into an error it doesn't delete the agent.

# This simple agent uses the Code Interpreter tool to answer coding questions. 
# Apart from the basic code from the documentation, it has been modified to take multiple subsequent user inputs for the coding question instead of hardcoding it.
# After the user inputs a question, the agent will respond with the answer, and the user can continue to ask more questions until they type 'exit'.
# At the end, the agent is deleted to clean up resources.

# Load environment variables from SimpleAgent.env file
load_dotenv("Credentials.env")

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
bing_connection= os.environ["BING_CONNECTION"]
print("starting creation of agent")

# Create an AIProjectClient instance
project_client = AIProjectClient(
endpoint=project_endpoint,
credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
)

code_interpreter = CodeInterpreterTool()
bing= BingGroundingTool(connection_id=bing_connection)

#Tool: Azure AI Search
azure_ai_conn_id= project_client.connections.get_default(ConnectionType.AZURE_AI_SEARCH).id
index_name= "hotels-sample-index-1"
ai_search= AzureAISearchTool(
    index_connection_id=azure_ai_conn_id,
    index_name=index_name,
    query_type=AzureAISearchQueryType.SIMPLE,  # Use semantic search for better results
    top_k=3, # Return top 3 results
    filter="",
)
print(f"Created Azure AI Search tool")


# Create an agent with the Bing Grounding tool
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
    name="tool-agent",  # Name of the agent
    instructions="""
    You are an AI assistant with 3 capabilities:

    1. You can interpret and answer coding questions using the Code Interpreter tool.
    2. You can answer questions about hotels using the documents in the AI Search tool.
    3. You can use the Bing Grounding tool to fetch real-time information from the web.
    
        Decide which tool to use based on the user's query.
    """,
    tools=code_interpreter.definitions + ai_search.definitions + bing.definitions,  # Combine both tool definitions
    tool_resources= ai_search.resources
)
print(f"Created agent, ID: {agent.id}")

# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

#Instead of hardcoding the message content, we can take user input
#Further addition: We can keep asking the user for input until they type 'exit'
userinput= ""
while userinput.lower() != "exit":
    userinput = input("Please enter your question (type 'exit' to quit): ")
    content= userinput  # Get user input for message content

    # Add a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",  # Role of the message sender
        content= content,  # Message content
    )
    #print(f"Created message, ID: {message['id']}")
    
    # Create and process an agent run
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    #print(f"Run finished with status: {run.status}")
    
    # Check if the run failed
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    
    # Fetch and log all messages
    messages = project_client.agents.messages.list(thread_id=thread.id)
    messages_list = list(messages)  # Convert ItemPaged to list
    if messages_list:
        latest_message = messages_list[0] # In the messages list, the first message is the latest one.
        # Extract just the text content from the message
        text_content = latest_message.content[0].text.value
        print(f"Agent: {text_content}")
    #for message in messages_list:
    #    print(f"Role: {message.role}, Content: {message.content}")
    
# Delete the agent when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")