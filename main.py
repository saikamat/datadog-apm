from flask import Flask, render_template_string
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
@app.route("/predictions")
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
        return f"Error: Failed to fetch data. Status code: {response.status_code}", response.status_code

    predictions = response.json().get('response', [])
    if not predictions:
        return "No predictions found", 404

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

    # Construct the HTML response
    html_response = f"""
    <html>
    <head>
        <title>Football Predictions</title>
    </head>
    <body>
        <h1>Basic Information</h1>
        <p>League: {league_name} ({league_country})</p>
        <p>Season: {season}</p>
        <p>Home Team: {home_team}</p>
        <p>Away Team: {away_team}</p>

        <h1>Predictions</h1>
        <p>Predicted Winner: {predicted_winner}</p>
        <p>Win or Draw: {win_or_draw}</p>
        <p>Advice: {advice}</p>
        <p>Percentage Chances: Home {percent_home}, Draw {percent_draw}, Away {percent_away}</p>

        <h1>Team Statistics</h1>
        <h2>{home_team} Statistics</h2>
        <p>Last 5 Form: {home_team_form}</p>
        <p>Goals Scored (Last 5): {home_team_goals_for}</p>
        <p>Goals Conceded (Last 5): {home_team_goals_against}</p>

        <h2>{away_team} Statistics</h2>
        <p>Last 5 Form: {away_team_form}</p>
        <p>Goals Scored (Last 5): {away_team_goals_for}</p>
        <p>Goals Conceded (Last 5): {away_team_goals_against}</p>

        <h1>Head to Head</h1>
        <p>Number of previous matches: {len(h2h_matches)}</p>
        <ul>
            {''.join([
                f"<li>Match {i+1} ({match['fixture']['date'][:10]}): {match['teams']['home']['name']} {match['goals']['home']}-{match['goals']['away']} {match['teams']['away']['name']}</li>"
                for i, match in enumerate(h2h_matches[:3])
            ])}
        </ul>

        <h1>Comparison Data</h1>
        <ul>
            {''.join([
                f"<li>{metric.capitalize()}: Home {values['home']}, Away {values['away']}</li>"
                for metric, values in comparison_data.items()
            ])}
        </ul>

        <h1>Yellow Cards for Home Team</h1>
        <ul>
            {''.join([
                f"<li>{time_range}: {data['total']} cards ({data['percentage']})</li>"
                for time_range, data in yellow_cards.items()
                if data['total'] is not None
            ])}
        </ul>
    </body>
    </html>
    """

    return html_response

if __name__ == "__main__":
    app.run()