import requests
from pprint import pprint
from typing import Annotated
from crewai.tools import tool

BASE_URL = "https://api.nal.usda.gov/fdc"
API_KEY = "AuqC2MjMYJlablZEiR17Q2HgULZifkgOhs6YyybH"

"""
curl -X 'GET' \
  'https://api.nal.usda.gov/fdc/v1/foods/search?query=cheddar%20cheese&dataType=Foundation,SR%20Legacy&pageSize=25&pageNumber=2&sortBy=dataType.keyword&sortOrder=asc&brandOwner=Kar%20Nut%20Products%20Company' \
  -H 'accept: application/json'
"""


def parse_food_info(food: dict):
    try:
        info = {}
        info["name"] = food["description"]
        info["serving_unit"] = food["servingSizeUnit"]
        info["serving_size"] = food["servingSize"]
        calories_l = [
            nutrient["value"] 
            for nutrient in food["foodNutrients"]if nutrient["nutrientId"] == 1008
        ]

        info["calories"] = calories_l[0]
        return info
    except KeyError as e:
        return

def _search_foods(query: str, data_types: list[str] = [], page_size: int = 5, page_number: int = 1, sort_by: str = None, sort_order: str = "asc", brand_owner: str = None):
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
    return response.json()

@tool
def search_ingredient(query: Annotated[str, "The name of the food to search for"]):
    """Search for the caloric value of this ingredient, relative to a portion size."""
    response_obj = _search_foods(query)

    parsed_foods = []
    for food in response_obj["foods"]:
        parsed_food = parse_food_info(food)
        if parsed_food is not None:
            parsed_foods.append(parsed_food)
    return parsed_foods[0]
    


if __name__ == "__main__":
    result = search_ingredient("chicken")
    pprint(result)
    

