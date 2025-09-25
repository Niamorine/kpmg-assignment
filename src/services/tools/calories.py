from typing import Literal, Annotated
from pydantic import Field
from crewai.tools import tool
from colorama import Fore


def _pounds_to_kg(pounds: float) -> float:
    return pounds * 0.45359237


def _feet_inches_to_cm(feet: int, inches: int) -> float:
    total_inches = feet * 12 + inches
    return total_inches * 2.54


def _calculate_bmr(age: int, weight_lb: float, height_ft: int, height_in: int, sex: str = "male") -> float:
    """
    Compute BMR with Mifflin formula
    This is the base value for a day
    """
    weight_kg = _pounds_to_kg(weight_lb)
    height_cm = _feet_inches_to_cm(height_ft, height_in)
    
    if sex == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def _calories_from_activity(weight_lb: float, duration_min: int, intensity: str) -> float:
    """
    Estimates calories spent during physical activity using MET values.
    Intensity can be: "none", "low", "medium", "high".
    """
    mets_values = {
        "none": 0,
        "low": 3,     # ex: yoga
        "medium": 6,  # ex: running
        "high": 8     # ex: rock climbing
    }
    
    weight_kg = _pounds_to_kg(weight_lb)
    mets = mets_values.get(intensity.lower(), 0)
    
    # Formule https://www.healthline.com/health/what-are-mets#calorie-connection
    calories_per_min = (mets * 3.5 * weight_kg) / 200
    return calories_per_min * duration_min

@tool
def calculate_daily_caloric_needs(
    age: Annotated[int, "Age in years"],
    weight_lb: Annotated[float, "Weight in pounds"],
    height_ft: Annotated[int, "Feet component of the height"],
    height_in: Annotated[int, "Inches component of the height"],
    activity_duration: Annotated[int, "Activity duration in minutes"],
    activity_intensity: Annotated[Literal["none", "low", "medium", "high"], "Intensity during activity"]
) -> dict:
    """
    Calculates the total daily energy expenditure (TDEE) in calories.
    If there's no activity for the day, select "none" as the intensity.
    """
    print(Fore.RED + f"Calculate calories called with age={age}, weight_lb={weight_lb}, height_ft={height_ft}, height_in={height_in}, activity_duration={activity_duration}, activity_intensity={activity_intensity}" + Fore.RESET)

    sex: str = "male"
    activity_factor: float = 1.2

    bmr = _calculate_bmr(age, weight_lb, height_ft, height_in, sex)
    base_tdee = bmr * activity_factor # user sedentary factor
    activity_cals = _calories_from_activity(weight_lb, activity_duration, activity_intensity)
    total_tdee = base_tdee + activity_cals
    
    # return {
    #     "BMR": round(bmr, 2),
    #     "Base_TDEE": round(base_tdee, 2),
    #     "Activity_Cals": round(activity_cals, 2),
    #     "Total_TDEE": round(total_tdee, 2)
    # }
    return total_tdee

@tool
def calculate_target_calories(
    daily_needs: Annotated[float, "The daily caloric needs."],
    objective: Annotated[Literal["loss", "gain", "maintain"], "The objective in terms of weight."]
) -> float:
    """Calculate the target calories for a day, using the calories needs and the objective."""
    percent = 0.15
    if objective == "loss":
        return daily_needs * (1 - percent)
    elif objective == "gain":
        return daily_needs * (1 + percent)
    else: 
        return daily_needs


if __name__ == "__main__":
    result = calculate_daily_caloric_needs.invoke({
        "age": 45,
        "weight_lb": 300,
        "height_ft": 6,
        "height_in": 5,
        "activity_duration": 120,
        "activity_intensity": "high"
    })
    print(result)
