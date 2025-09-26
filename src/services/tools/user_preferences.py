from crewai.tools import tool


@tool
def get_user_preferences():
    """Return the user preferences regarding what food they like."""
    with open("food_preferences 1.json", "r") as f:
        food_preferences = f.read()
    return food_preferences

