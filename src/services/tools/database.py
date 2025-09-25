from typing import Annotated, Literal
import sqlite3
from crewai.tools import tool
from colorama import Fore


"""
Table activity_calendar
id | day_of_week | activity_name | duration_mins | intensity
1 | monday | rock climbing | 120 | high
"""

days_of_the_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

@tool
def read_calendar(
        day_of_week: Annotated[Literal[*days_of_the_week + ["none"]], "The day to lookup for in the calendar. Putting none will look at the whole week."]): # type: ignore
    """Read the user's calendar. The calendar contains the day, the name of the activity
    """
    print(Fore.BLUE + f"Read calendar called with {day_of_week=}," + Fore.RESET)

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
    # return rows

if __name__ == "__main__":
    print(read_calendar.invoke({"day_of_week": "monday"}))