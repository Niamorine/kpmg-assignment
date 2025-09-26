from typing import Annotated, Literal
import sqlite3
from crewai.tools import tool


days_of_the_week: list[str] = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

@tool
def read_calendar(
        day_of_week: Annotated[Literal[*days_of_the_week + ["none"]], "The day to lookup for in the calendar. Putting none will look at the whole week."]): # type: ignore
    """Read the user's calendar. The calendar contains the day, the name of the activity
    """

    if day_of_week not in [""] + days_of_the_week:
        return "Invalid day of the week given."
    conn = sqlite3.connect('meal_prep 1.db')
    cursor = conn.cursor()

    select_query = f"""
        SELECT day_of_week, activity_name, duration_mins, intensity
        FROM activity_calendar"""
    if day_of_week:
        select_query += f" WHERE day_of_week = '{day_of_week}'"

    cursor.execute(select_query)
    
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "day_of_week": row[0],
            "activity_name": row[1],
            "duration_mins": row[2],
            "intensity": row[3]
        })
    return result

@tool
def get_existing_meals():
    """Retrieve the existing meals that the user will eat this week."""
    conn = sqlite3.connect('meal_prep 1.db')
    cursor = conn.cursor()

    select_query = """
        SELECT day_of_week, meal_type, food_item, calories
        FROM meal_plan
    """
    cursor.execute(select_query)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "day_of_week": row[0],
            "meal_type": row[1],
            "food_items": row[2],
            # "calories": row[3]
        })
    return result


# Only for initial setup
def insert_meal(
        day_of_week: Annotated[Literal[*days_of_the_week], "The day of this meal."], # type: ignore
        meal_type: Annotated[Literal["breakfast", "lunch", "dinner"], "The type of meal this is."],
        ingredients: Annotated[list[str], "The ingredients in the meal."]
):
    conn = sqlite3.connect('meal_prep 1.db')
    cursor = conn.cursor()
    food_item = " ".join(ingredients)
    insert_query = """
        INSERT INTO meal_plan (day_of_week, meal_type, food_item)
        VALUES (?, ?, ?)
    """
    cursor.execute(insert_query, (day_of_week, meal_type, food_item))
    conn.commit()
    conn.close()
    return {"status": "success", "day_of_week": day_of_week, "meal_type": meal_type, "food_item": food_item}

# Only used to debug
def clear_meal_plan_table():
    conn = sqlite3.connect('meal_prep 1.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meal_plan")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_meal(
        "monday",
        "breakfast",
        ["banana", "eggs", "greek yogurt"]
    )

    insert_meal(
        "monday",
        "lunch",
        ["chiken breast", "quinoa", "broccoli"]
    )

    insert_meal(
        "monday",
        "dinner",
        ["salmon", "sweet potato", "asparagus"]
    )
