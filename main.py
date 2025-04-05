from flask import Flask
import requests
from ddtrace import tracer
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load API key from environment variable
RAPIDAPI_KEY = os.getenv('RAPID_API_KEY')
RAPIDAPI_HOST = 'api-football-v1.p.rapidapi.com'
BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3/predictions'

@tracer.wrap(name='my_resource1')
@app.route("/api")
def hello_world():
    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    params = {
        'fixture': 198772
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}, response.status_code

    predictions = response.json().get('response', [])
    if not predictions:
        return {"error": "No predictions found"}, 404

    match_data = predictions[0]

    # Basic Information
    league_name = match_data['league']['name']
    league_country = match_data['league']['country']
    season = match_data['league']['season']
    home_team = match_data['teams']['home']['name']
    away_team = match_data['teams']['away']['name']

    # Predictions
    predicted_winner = match_data['predictions']['winner']['name']
    win_or_draw = match_data['predictions']['win_or_draw']
    advice = match_data['predictions']['advice']
    percent_home = match_data['predictions']['percent']['home']
    percent_draw = match_data['predictions']['percent']['draw']
    percent_away = match_data['predictions']['percent']['away']

    # Team Statistics
    home_team_form = match_data['teams']['home']['last_5']['form']
    home_team_goals_for = match_data['teams']['home']['last_5']['goals']['for']['total']
    home_team_goals_against = match_data['teams']['home']['last_5']['goals']['against']['total']
    away_team_form = match_data['teams']['away']['last_5']['form']
    away_team_goals_for = match_data['teams']['away']['last_5']['goals']['for']['total']
    away_team_goals_against = match_data['teams']['away']['last_5']['goals']['against']['total']

    # Head to Head
    h2h_matches = match_data['h2h']

    # Comparison Data
    comparison_data = match_data['comparison']

    # Yellow Cards for Home Team
    yellow_cards = match_data['teams']['home']['league']['cards']['yellow']

    # Construct the response
    response_data = {
        "basic_information": {
            "league": f"{league_name} ({league_country})",
            "season": season,
            "home_team": home_team,
            "away_team": away_team
        },
        "predictions": {
            "predicted_winner": predicted_winner,
            "win_or_draw": win_or_draw,
            "advice": advice,
            "percentages": {
                "home": percent_home,
                "draw": percent_draw,
                "away": percent_away
            }
        },
        "team_statistics": {
            "home_team": {
                "form": home_team_form,
                "goals_for": home_team_goals_for,
                "goals_against": home_team_goals_against
            },
            "away_team": {
                "form": away_team_form,
                "goals_for": away_team_goals_for,
                "goals_against": away_team_goals_against
            }
        },
        "head_to_head": {
            "number_of_previous_matches": len(h2h_matches),
            "matches": [
                {
                    "date": match['fixture']['date'][:10],
                    "home_team": match['teams']['home']['name'],
                    "away_team": match['teams']['away']['name'],
                    "home_goals": match['goals']['home'],
                    "away_goals": match['goals']['away']
                }
                for match in h2h_matches
            ]
        },
        "comparison_data": {
            metric: {
                "home": values['home'],
                "away": values['away']
            }
            for metric, values in comparison_data.items()
        },
        "yellow_cards": {
            time_range: {
                "total": data['total'],
                "percentage": data['percentage']
            }
            for time_range, data in yellow_cards.items()
            if data['total'] is not None
        }
    }

    return response_data

if __name__ == "__main__":
    app.run()