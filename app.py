from flask import Flask, request, jsonify
import requests
import redis
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

# Initialize the app
app = Flask(__name__)

# Load API Key and Redis connection string from .env
API_KEY = os.getenv("WEATHER_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")

# Initialize Redis
redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

# Rate limiter (5 requests per minute per IP)
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

# Visual Crossing API endpoint
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

# Cache expiration time (12 hours)
CACHE_EXPIRATION = 43200  # 12 hours in seconds


def fetch_weather_data(city):
    """Fetch weather data from Visual Crossing API."""
    url = f"{BASE_URL}{city}"
    params = {
        "key": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None


@app.route("/weather", methods=["GET"])
@limiter.limit("5 per minute")
def get_weather():
    """API endpoint to get weather data for a given city."""
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    # Check if data is in cache
    cached_data = redis_client.get(city)
    if cached_data:
        print("Cache hit")
        return jsonify({"source": "cache", "data": cached_data})

    print("Cache miss")
    # Fetch new weather data from Visual Crossing API
    weather_data = fetch_weather_data(city)

    if not weather_data:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    # Save weather data in cache with expiration time (12 hours)
    redis_client.setex(city, CACHE_EXPIRATION, str(weather_data))

    return jsonify({"source": "api", "data": weather_data})


if __name__ == "__main__":
    app.run(debug=True)
