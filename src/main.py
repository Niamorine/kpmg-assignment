from time import time
import argparse
from dotenv import load_dotenv

from crewai import Crew, Process

from agents import calendar_agent, nutritionist_agent, meal_planner_agent, presenter_agent
from tasks import activity_task, target_calories_task, meals_task, present_task

load_dotenv()

def get_args():
    parser = argparse.ArgumentParser(description="Meal planning crew")
    parser.add_argument("--age", type=int, default=45, help="Age of the user")
    parser.add_argument("--weight", type=float, default=300, help="Weight of the user (lbs)")
    parser.add_argument("--height_ft", type=int, default=6, help="Height in feet")
    parser.add_argument("--height_in", type=int, default=5, help="Height in inches")
    parser.add_argument("--day", type=str, default="tuesday", help="Day of the week")
    parser.add_argument("--objective", type=str, choices=["loss", "gain", "maintain"], default="loss", help="Objective in terms of weight")

    args = parser.parse_args()
    return args

meals_crew = Crew(
    agents=[calendar_agent, nutritionist_agent, meal_planner_agent, presenter_agent],
    tasks=[activity_task, target_calories_task, meals_task, present_task],
    process=Process.sequential,
    verbose=True
)


def main():
    args = get_args()

    print(f"Running with args: {args}")

    t_begin = time()
    result = meals_crew.kickoff(
        inputs={
            "age": args.age,
            "weight": args.weight,
            "height_ft": args.height_ft,
            "height_in": args.height_in,
            "day": args.day,
            "objective": args.objective
        }
    )
    print(result)
    print(f"Total time taken: {time() - t_begin}")


if __name__ == "__main__":
    main()
