import requests
from pprint import pprint
from typing import Annotated
from crewai.tools import tool
import concurrent.futures

BASE_URL = "https://api.nal.usda.gov/fdc"
API_KEY = "AuqC2MjMYJlablZEiR17Q2HgULZifkgOhs6YyybH"



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
    except KeyError as e:
        return

def _search_food_info(fd_cid: int, nutrients_number: int = 208) -> dict:
    url = f"{BASE_URL}/v1/food/{fd_cid}"
    params = {
        "format": "full",
        "nutrients": nutrients_number,
        "api_key": API_KEY
    }
    headers = {
        "accept": "application/json"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    food_infos = response.json()
    
    result = {}

    nutrients = food_infos["foodNutrients"]

    for nutrient in nutrients:
        if nutrient["nutrient"].get("number") == str(nutrients_number):
            result["amount_of_calories"] = nutrient["amount"]
            break

    return result

def _search_ingredient(query: str, data_types: list[str] = [], page_size: int = 5, page_number: int = 1, sort_by: str = None, sort_order: str = "asc", brand_owner: str = None):
    url = f"{BASE_URL}/v1/foods/search"
    params = {
        "query": query,
        "dataType": ",".join(data_types),
        "pageSize": page_size,
        "pageNumber": page_number,
        "sortBy": sort_by,
        "sortOrder": sort_order,
        "brandOwner": brand_owner,
        "api_key": API_KEY
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
    
