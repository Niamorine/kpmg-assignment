import os
from crewai import Agent, LLM
from tools.calories import calculate_target_calories, calculate_daily_caloric_needs
from tools.database import read_calendar, get_existing_meals
from tools.food_api_client import search_ingredients
from tools.user_preferences import get_user_preferences



llm = LLM(
    model="watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    base_url=os.environ["WATSONX_URL"],
    project_id=os.environ["WATSONX_PROJECT_ID"],
    temperature=0.2
)

creative_llm = LLM(
    model="watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    base_url=os.environ["WATSONX_URL"],
    project_id=os.environ["WATSONX_PROJECT_ID"],
    temperature=1.0,  # Higher temperature for more creativity
)


calendar_agent = Agent(
    role="User Planning Assistant",
    goal="Read the user's calendar and provide factual information.",
    backstory="You have access to the calendar which you use to retrieve information.",
    tools=[read_calendar],
    llm=llm,
    verbose=True
)

nutritionist_agent = Agent(
    role="Nutritionist Expert",
    goal="Explain to the user how much calories they need for a day, depending on their physical characteristics and daily physical activity.",
    backstory="You calculate the daily calories needed with the right information, followed by the target for the user.",
    tools=[calculate_daily_caloric_needs, calculate_target_calories],
    llm=llm,
    verbose=True
)


meal_planner_agent = Agent(
    role="Personalized Meal Planner",
    goal="Using user preferences and their target calories, you provide daily meal plan to help them reach their target calories.",
    backstory="You can check what the user likes by looking at their preferences. You avoid suggesting meals that are too similar to those already planned by the user. You search information about ingredients and compose meals with just the right amount of calories.",
    tools=[get_user_preferences, get_existing_meals, search_ingredients],
    llm=creative_llm,
    verbose=True
)


presenter_agent = Agent(
    role="Results Presentation Specialist",
    goal="Present the user's daily activity, target calories, and meal plan in a clear, engaging, and user-friendly format.",
    backstory="You are an expert in communicating health and nutrition information. You excel at organizing complex data into easy-to-read reports, ensuring the user feels informed and motivated to follow their meal plan.",
    llm=llm,
    verbose=True
)
