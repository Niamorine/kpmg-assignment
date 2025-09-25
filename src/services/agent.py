from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import os
from dotenv import load_dotenv
from pprint import pprint
from .tools.calories import calculate_target_calories, calculate_daily_caloric_needs
from .tools.database import read_calendar

load_dotenv()

WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers"""
    return a + b

# Create the agent
memory = MemorySaver()
# model_name = "openai/gpt-oss-120b"
model_name = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"
model = init_chat_model(model_name, model_provider="ibm", project_id=WATSONX_PROJECT_ID)
tools = [calculate_daily_caloric_needs, read_calendar]
# tools = [multiply, add]
model_with_tools = model.bind_tools(tools)
agent_executor = create_react_agent(
    model_with_tools,
    tools,
    checkpointer=memory,
    prompt="You are a friendly assistant for humans. "
    "Use the tools to answer their questions. "
)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "meals_agent"}}




    user_message = {
       "role": "user",
        # "content": "I am 45 years old, I weight 300 pounds, I measure 6' 5''"
        # " and I do high intensity sports for 2 hours a day."
        # " How many calories do you recommend I take?",
        "content": "I am 45 years old, I weight 300 pounds, I measure 6' 5''. "
        "How many calories do you recommend I take Saturday?",
        # "content": "I want you to multiply 2 with 3. Then, add 4 to the first result."
    }

    messages = [user_message]
    
    # response = agent_executor.invoke({"messages": messages}, config, stream_mode="values")
    # pprint(response)
    
    # Using my calendar and food preferences, Give me 3 meals recommendation for each day.
    for step in agent_executor.stream(
        {"messages": messages}, config, stream_mode="values"
    ):
        step["messages"][-1].pretty_print()




