import os
import requests
from bs4 import BeautifulSoup

from pydantic import BaseModel
from langchain_core.tools import StructuredTool
from langchain_core.tools import BaseTool, StructuredTool
from langchain_openai import AzureChatOpenAI
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults

from langgraph.prebuilt import create_react_agent

from common.prompts import BING_PROMPT_TEXT

from IPython.display import Markdown, HTML, display  

def printmd(string):
    display(Markdown(string.replace("$","USD ")))



from dotenv import load_dotenv
load_dotenv("credentials.env")

# Set the ENV variables that Langchain needs to connect to Azure OpenAI
#os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"]

COMPLETION_TOKENS = 2000

llm = AzureChatOpenAI(deployment_name=os.environ["GPT4o_DEPLOYMENT_NAME"], 
                      azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                      api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                      api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                      temperature=0.5, max_tokens=COMPLETION_TOKENS, 
                      streaming=True)

api_wrapper = BingSearchAPIWrapper(bing_subscription_key=os.getenv("BING_SUBSCRIPTION_KEY"))
bing_tool = BingSearchResults(api_wrapper=api_wrapper, 
                              num_results=10,
                              name="Searcher",
                              description="useful to search the internet")

def parse_html(content) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    text_content_with_links = soup.get_text()
    # Split the text into words and limit to the first 10,000
    limited_text_content = ' '.join(text_content_with_links.split()[:10000])
    return limited_text_content

def fetch_web_page(url: str) -> str:
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'}
    response = requests.get(url, headers=HEADERS)
    return parse_html(response.content)

web_fetch_tool = StructuredTool.from_function(
    func=fetch_web_page,
    name="WebFetcher",
    description="useful to fetch the content of a url"
)

tools = [bing_tool, web_fetch_tool]

# Uncoment to see the prompt
printmd(BING_PROMPT_TEXT)

graph = create_react_agent(llm, tools=tools, state_modifier=BING_PROMPT_TEXT)

# QUESTION = "Create a list with the main facts on What is happening with the oil supply in the world right now?"
# QUESTION = "How much is 50 USD in Euros and is it enough for an average hotel in Madrid?"
# QUESTION = "My son needs to build a pinewood car for a pinewood derbi, how do I build such a car?"
QUESTION = "I'm planning a vacation to Greece, tell me budget for a family of 4, in Summer, for 7 days including travel, lodging and food costs"
# QUESTION = "Who won the 2023 superbowl and who was the MVP?"
# QUESTION = """
# compare the number of job opennings (provide the exact number), the average salary within 15 miles of Dallas, TX, for these ocupations:

# - ADN Registerd Nurse 
# - Occupational therapist assistant
# - Dental Hygienist
# - Certified Personal Trainer


# Create a table with your findings. Place the sources on each cell.
# """


async def stream_graph_updates_async(graph, user_input: str):
    inputs = {"messages": [("human", user_input)]}
    output = ""
    printmd("prompt:" + BING_PROMPT_TEXT)
    async for event in graph.astream_events(inputs, version="v2"):
        if (event["event"] == "on_chat_model_stream"):
            # Print the content of the chunk progressively
            print(event["data"]["chunk"].content, end="", flush=True)
            output += event["data"]["chunk"].content
        elif (event["event"] == "on_tool_start"  ):
            #print("\n--")
            output += f"\n--\nCalling tool: {event['name']} with inputs: {event['data'].get('input')}\n--\n"
            #print(f"Calling tool: {event['name']} with inputs: {event['data'].get('input')}")
            #print("--")
    return output


#await stream_graph_updates_async(graph, QUESTION)

"""
QUESTION = "How much is 50 USD in Euros and is it enough for an average hotel in Madrid?"

try:
    response = graph.invoke({"messages": [("human", QUESTION)]})
except Exception as e:
    response = str(e)

printmd(response["messages"][-1].content)
"""

QUESTION = "information on how to deal with wasps in homedepot.com"
# QUESTION = "in target.com, find how what's the price of a Nesspresso coffee machine and of a Keurig coffee machine"
# QUESTION = "in microsoft.com, find out what is the latests news on quantum computing"


import asyncio
result = asyncio.run(stream_graph_updates_async(graph, QUESTION))
printmd(result)
