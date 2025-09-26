import requests
from pprint import pprint
from typing import Annotated
import os
import concurrent.futures
from crewai.tools import tool


from dotenv import load_dotenv

load_dotenv()

FOOD_API_URL = os.getenv("FOOD_API_URL")
FOOD_API_KEY = os.getenv("FOOD_API_KEY")

def _parse_food_info(food: dict):
    try:
        info = {}
        info["name"] = food["description"]
        calories_l = [
            nutrient["value"] 
            for nutrient in food["foodNutrients"]if nutrient["nutrientId"] == 1008
        ]

        info["calories_per_100g"] = calories_l[0]

        return info
    except KeyError as e: # Sometimes a key would be missing
        return


def _search_ingredient(query: str, data_types: list[str] = [], page_size: int = 5, page_number: int = 1, sort_by: str = None, sort_order: str = "asc", brand_owner: str = None):
    url = f"{FOOD_API_URL}/v1/foods/search"
    params = {
        "query": query,
        "dataType": ",".join(data_types),
        "pageSize": page_size,
        "pageNumber": page_number,
        "sortBy": sort_by,
        "sortOrder": sort_order,
        "brandOwner": brand_owner,
        "api_key": FOOD_API_KEY
    }
    headers = {
        "accept": "application/json"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    response_obj = response.json()
    food = response_obj["foods"][0] # Keep only the first

    parsed_food = _parse_food_info(food)

    return parsed_food

    
@tool
def search_ingredients(ingredients: Annotated[list[str], "The name of the ingredients to search for"]):
    """Search for the caloric value of each ingredient provided, relative to a portion size. Use this tool when you want to get information on many ingredients."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(_search_ingredient, ingredients))
    return results


if __name__ == "__main__":
    result = search_ingredients.run([
    "chicken breast",
    "salmon",
    "tuna",
    ])
    pprint(result)
    
