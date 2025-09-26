from crewai import Agent, Task, LLM, Crew, Process
import os
from .tools.calories import calculate_target_calories, calculate_daily_caloric_needs
from .tools.database import read_calendar
from .tools.food_api_client import search_ingredient
from time import time


from dotenv import load_dotenv

load_dotenv()



llm = LLM(
    # model="watsonx/openai/gpt-oss-120b",
    model="watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
    base_url=os.environ["WATSONX_URL"],
    project_id=os.environ["WATSONX_PROJECT_ID"]
)




agent = Agent(
    role="Nutritionist expert",
    goal="Give nutrition adivces.",
    backstory="An expert nutritionist.",
    tools=[read_calendar, calculate_daily_caloric_needs, calculate_target_calories, search_ingredient],
    llm=llm,
    verbose=True
)

age = 45
weight = 300
height_ft = 6
height_in = 5
day = "monday"
objective = "loss"

with open("food_preferences 1.json", "r") as f:
    food_preferences = f.read()

task = Task(
    description=f"""Give me three meals suggestions for {day} (breakfast, lunch, dinner).

Here are more detailed instructions:
I am {age} years old, I weight {weight} pounds, measure {height_ft}' {height_in}'' and my goal is to {objective} weight.

Here are my preferences :
{food_preferences}

To accomplish this task, you must:
1. Lookup the calendar and the day I am asking.
2. Use the characteristics I provided about myself to know what's my daily caloric needs.
3. Use my goal to calculate my calories target.
4. Use my preferences to search for ingredients and get their caloric values. Don't chose any from the one I dislike!
5. Adjusting portion size to meet the daily target, compose three meals for breakfast, lunch and dinner.
""",
    expected_output="Answer clearly by first citing what is the daily calories target. Then, continue with the three meals, their ingredients, and their caloric values, as well as the total caloric value for the day.",
    # output_pydantic=
)

"""
Given this target calories and user preferences, elaborate 3 meals for the day. You can search for nutrients.
You must first calculate the number of calories required
"""

t_begin = time()
result = agent.execute_task(task)

print(result)

print(f"Total time taken: {time() - t_begin}")


"""
chicken breast: 284g 165 calories
quinoa: 28g 357 calories
broccoli: 85g 24 calories
salmon: 151g 139 calories
sweet potato: 312g 106 calories
oatmeal: 45g 1580 calories
banana: 32g 312 calories
almonds: 30g 633 calories
asparagus: 85g 18 calories


"""