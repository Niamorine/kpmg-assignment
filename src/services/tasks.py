from crewai import Task
from .agents import calendar_agent, nutritionist_agent, meal_planner_agent, presenter_agent



activity_task = Task(
    description="Retrieve the physical activity of the user on {day} from their calendar.",
    expected_output="A simple sentence with the name of the activity, the duration in minutes and the intensity.",
    agent=calendar_agent
)

target_calories_task = Task(
    description="Determine the user's recommended target calorie intake for {day} to help them achieve their goal to {objective} weight. The user is {age} years old, weighs {weight} pounds, and is {height_ft} feet {height_in} inches tall.",
    expected_output="A clear statement of the user's target calorie intake for {day}, including a brief explanation of how this number was calculated based on their physical characteristics and weight objective.",
    agent=nutritionist_agent
)

meals_task = Task(
    description=(
        "Design a daily meal plan for {day} consisting of three distinct meals: breakfast, lunch, and dinner. "
        "Ensure the total calorie intake closely matches the user's target calories for the day. "
        "Take into account the user's food preferences and avoid repeating meals already planned. "
        "For each meal, specify the name, total calories, and provide a detailed list of ingredients with their portion sizes and individual calorie counts."
    ),
    expected_output=(
        "A structured meal plan for {day} with three meals (breakfast, lunch, dinner). "
        "For each meal, include: meal name, total calories, and a breakdown of ingredients with portion sizes and calories. "
        "Also, provide the combined total calories for all meals."
    ),
    agent=meal_planner_agent
)

present_task = Task(
    description="Present the results (physical activity of the day, target calories, meal plan to achieve that) in a user-friendly format to the user.",
    expected_output="A report in markdown format with 2 sections: 1. Target Calories for {day}: Explain the number with the physical activity. 2. Meals Plan for {day}: Nicely present the three meals in order, for each ingredient give the portion size and calories.",
    output_file="Meal Plan for {day}.md",
    agent=presenter_agent
)
