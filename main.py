# Load environment variables from a .env file.
from dotenv import load_dotenv

# Define structured output models using Pydantic
from pydantic import BaseModel

# Langchain imports that we will use to interact with Mistral
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import SystemMessage

# Import from langgraph for agent creation
from langgraph.prebuilt import create_react_agent

# Custom tools that we will use. These are pulled from our tools.py
from tools import scrape_tool, search_tool, save_tool  

# Pulling our Mistral API key from our .env file.
load_dotenv()

# Define the structure of each lead in the output
class LeadResponse(BaseModel):
    company: str
    contact_info: str
    email: str
    summary: str
    outreach_message: str
    tools_used: list[str]

# Define a list structure to hold multiple leads
class LeadResponseList(BaseModel):
    leads: list[LeadResponse]

# Determining which AI model we will use, in this case, Mistral Large
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.1
)

# Tell Mistral how to format the response using the Pydantic schema
parser = PydanticOutputParser(pydantic_object=LeadResponseList)

# System prompt with instructions
system_prompt = f"""
You are a sales enablement assistant.
1. Use the 'search_and_scrape' tool to find exactly 5 local small businesses in Vancouver, British Columbia, from a variety of industries, that might need IT services.
2. For each company identified, use the 'search_web' tool to gather detailed information from DuckDuckGo.
3. Analyze the searched website content to provide:
    - company: The company name
    - contact_info: Any available contact details
    - summary: A brief qualification based on the scraped website content, focusing on their potential IT needs even if they are not an IT company.
    - email addresses
    - outreach message
    - tools_used: List tools used        

Do not include extra text beyond the formatted output and the save confirmation message.
4. Return the output as a list of 5 entries in this format: {parser.get_format_instructions()}
5. After formatting the list of 5 entries, use the 'save_to_txt' tool to send the json format to the text file. 
6. If the 'save' tool runs, say that you ran it. If you did not run the 'save' tool, say that you could not run it.
"""

# List the tools we are telling our LLM to use from our tools.py file
tools = [scrape_tool, search_tool, save_tool]

# Create the agent using LangGraph's create_react_agent
agent_executor = create_react_agent(
    model=llm,
    tools=tools
)

# Define the query that kicks off the lead generation process
query = "Find and qualify exactly 5 local leads in Vancouver for IT Services. No more than 5 small businesses."

# Run the agent with the query, including system message in the messages list
print("Starting lead generation process with Mistral...")
print("-" * 50)

try:
    # Include system prompt as a system message
    result = agent_executor.invoke({
        "messages": [
            SystemMessage(content=system_prompt),
            ("user", query)
        ]
    })
    
    # Get the last message from the agent
    last_message = result["messages"][-1]
    output_text = last_message.content
    
    print("\nAgent Output:")
    print(output_text)
    print("-" * 50)
    
    # Try to parse the structured output
    try:
        structured_response = parser.parse(output_text)
        print("\nParsed Structured Response:")
        print(structured_response)
    except Exception as e:
        print(f"\nError parsing response: {e}")
        print("Raw output saved above.")
        
except Exception as e:
    print(f"Error running agent: {e}")
    import traceback
    traceback.print_exc()