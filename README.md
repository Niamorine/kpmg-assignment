# Meal Planner Agent

This project was realized by Romain Le Métayer as an assigment for a technical interview with KPMG.

It is a personalized meal planning AI agent powered by CrewAI and IBM WatsonX LLM. This tool generates daily meal plans tailored to user preferences, physical activity, and nutritional goals.

## Features

- Reads user food preferences from a JSON file
- Retrieves daily physical activity from a calendar
- Calculates recommended calorie intake based on user profile and activity
- Designs daily meal plans (breakfast, lunch, dinner) matching target calories
- Presents results in a user-friendly markdown report

## Project Structure

```
.
├── food_preferences 1.json
├── meal_prep 1.db
├── pyproject.toml
├── README.md
├── src
│   ├── agents.py
│   ├── main.py
│   ├── tasks.py
│   └── tools
│       ├── calories.py
│       ├── database.py
│       ├── food_api_client.py
│       └── user_preferences.py
└── uv.lock
```

- `src/agents.py`: Defines CrewAI agents and their roles.
- `src/tasks.py`: Specifies tasks for each agent.
- `src/main.py`: Entry point for running the meal planning workflow.
- `src/tools/`: Tools usable by the agents for calories calculation, database access, food API, and user preferences.
- `food_preferences 1.json`: User's food likes/dislikes.
- `.env`: API keys and configuration.


## Getting Started

1. **Install dependencies**  
   Make sure you have Python 3.12.10.  
   I used UV for managing the project. Run `uv sync` to install the dependencies.

2. **Configure environment**  
   Fill in `.env` with your API keys and URLs like this:

    ```conf
    # The API for retrieving food information
    FOOD_API_URL=https://api.nal.usda.gov/fdc
    FOOD_API_KEY=

    # I used WatsonX but you can use any LLM provider of your choice
    WATSONX_APIKEY=
    WATSONX_PROJECT_ID=
    WATSONX_URL=

    ```


3. **Run the planner**  
   ```
   uv run src/main.py --age 45 --weight 300 --height_ft 6 --height_in 5 --day tuesday --objective loss
   ```

   Arguments:
   - `--age`: User's age
   - `--weight`: Weight in pounds
   - `--height_ft`: Height's feet component
   - `--height_in`: Height's inches component
   - `--day`: Day of the week
   - `--objective`: Weight objective (`loss`, `gain`, `maintain`)

## Customization

- Update `food_preferences 1.json` to reflect your likes/dislikes.
- Add calendar data to `meal_prep 1.db` in table `activity_calendar` for activity tracking.

## Output

Results are printed to the console and saved as a markdown report.
