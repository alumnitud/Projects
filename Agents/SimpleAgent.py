import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool

# This simple agent uses the Code Interpreter tool to answer coding questions. 
# Apart from the basic code from the documentation, it has been modified to take multiple subsequent user inputs for the coding question instead of hardcoding it.
# After the user inputs a question, the agent will respond with the answer, and the user can continue to ask more questions until they type 'exit'.
# At the end, the agent is deleted to clean up resources.

# Load environment variables from SimpleAgent.env file
load_dotenv("Credentials.env")

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
print("starting creation of agent")
# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
)

code_interpreter = CodeInterpreterTool()
with project_client:
    # Create an agent with the Bing Grounding tool
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name="simple-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=code_interpreter.definitions,  # Attach the tool
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")
    
    #Instead of hardcoding the message content, we can take user input
    #Further addition: We can keep asking the user for input until they type 'exit'
    userinput= ""
    while userinput.lower() != "exit":
        userinput = input("Enter your coding question (type 'exit' to quit): ")
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