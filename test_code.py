import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable
RAPIDAPI_KEY = os.getenv('RAPID_API_KEY')
RAPIDAPI_HOST = 'api-football-v1.p.rapidapi.com'
BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3/predictions'

def fetch_predictions():
    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    params = {
        'fixture': 198772
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        return

    predictions = response.json().get('response', [])
    match_data = predictions[0]
    print("=== Basic Information ===")
    print(f"League: {match_data['league']['name']} ({match_data['league']['country']})")
    print(f"Season: {match_data['league']['season']}")
    print(f"Home Team: {match_data['teams']['home']['name']}")
    print(f"Away Team: {match_data['teams']['away']['name']}")

    print("\n=== Predictions ===")
    print(f"Predicted Winner: {match_data['predictions']['winner']['name']}")
    print(f"Win or Draw: {match_data['predictions']['win_or_draw']}")
    print(f"Advice: {match_data['predictions']['advice']}")
    print(f"Percentage Chances: Home {match_data['predictions']['percent']['home']}, Draw {match_data['predictions']['percent']['draw']}, Away {match_data['predictions']['percent']['away']}")
    print("\n=== Team Statistics ===")
    home_team = match_data['teams']['home']['name']
    away_team = match_data['teams']['away']['name']

    # Home team stats
    print(f"{home_team} Last 5 Form: {match_data['teams']['home']['last_5']['form']}")
    print(f"{home_team} Goals Scored (Last 5): {match_data['teams']['home']['last_5']['goals']['for']['total']}")
    print(f"{home_team} Goals Conceded (Last 5): {match_data['teams']['home']['last_5']['goals']['against']['total']}")

# Away team stats
    print(f"{away_team} Last 5 Form: {match_data['teams']['away']['last_5']['form']}")
    print(f"{away_team} Goals Scored (Last 5): {match_data['teams']['away']['last_5']['goals']['for']['total']}")
    print(f"{away_team} Goals Conceded (Last 5): {match_data['teams']['away']['last_5']['goals']['against']['total']}")
    
    print("\n=== Head to Head ===")
    print(f"Number of previous matches: {len(match_data['h2h'])}")

    print("\n=== Accessing Nested Data Example ===")
# 5. Example of accessing deeply nested data
    print("Yellow cards for home team by minute:")
    yellow_cards = match_data['teams']['home']['league']['cards']['yellow']
    for time_range, data in yellow_cards.items():
        if data['total'] is not None:
            print(f"  {time_range}: {data['total']} cards ({data['percentage']})")

    print("\n=== Comparison Data ===")
    # 6. Access comparison data
    for metric, values in match_data['comparison'].items():
        print(f"{metric.capitalize()}: Home {values['home']}, Away {values['away']}")

    # Print the results of the last 3 matches
        for i, match in enumerate(match_data['h2h'][:3]):
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            home_goals = match['goals']['home']
            away_goals = match['goals']['away']
            date = match['fixture']['date'][:10]  # Just the date part
            print(f"Match {i+1} ({date}): {home} {home_goals}-{away_goals} {away}")

if __name__ == "__main__":
    predictions = fetch_predictions()