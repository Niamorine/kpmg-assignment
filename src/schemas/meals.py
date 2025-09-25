from pydantic import BaseModel, Field


class Meal(BaseModel):
    name: str
    ingredients: list[str]
    calories: float

class DailyMeals(BaseModel):
    day_of_week: str
    meals: list = Field(..., min_items=3, max_items=3) # Exactly 3 meals a day


class MealsPlan(BaseModel):
    days: list[DailyMeals] = Field(..., min_items=7, max_items=7)  # Exactly 7 days in the plan


