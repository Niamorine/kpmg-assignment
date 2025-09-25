from fastapi import APIRouter
from ..schemas.meals import MealsPlan
from fastapi import Query
from enum import Enum
from fastapi import HTTPException

router = APIRouter(
    prefix="/meals",
)

class Objective(str, Enum):
    loss = "loss"
    gain = "gain"
    maintain = "maintain"

@router.get("/plan")
async def get_meals_plan(
    age: int = Query(..., ge=0),
    weight_lb: float = Query(..., ge=0),
    height_feet: int = Query(..., ge=0),
    height_inches: int = Query(..., ge=0, le=11),
    objective: Objective = Query(..., description="Objective: loss, gain, or maintain")
) -> str:
    # You can use age, weight, height_in_inches, and objective as needed
    return "MealsPlan"




"""
1. Compute 
"""
