# Weather API

## Overview
This project is a weather API built with Flask, which fetches weather data from a third-party weather service ([Visual Crossing API](https://www.visualcrossing.com/)). The application is designed to allow users to request weather data for a given city, with caching to optimize performance and rate limiting to control API usage.

## Features
- **Weather Data**: Fetches real-time weather data for a given city.
- **Caching**: Caches the weather data in Redis for 12 hours to avoid repeated API calls.
- **Rate Limiting**: Limits users to 5 requests per minute to prevent overloading the server.
- **Error Handling**: Provides error messages for missing or invalid parameters and failed API calls.

## Prerequisites
Before you begin, ensure you have the following:
- Python 3.6 or higher
- Redis server running
- A Visual Crossing API key

## Installation

### Step 1: Clone the Repository
```
git clone https://github.com/idorombaut/weather-api.git
cd weather-api
```

### Step 2: Install Redis
**On macOS (using Homebrew)**:  
If you're on macOS, you can install Redis using Homebrew:
```
brew install redis
```
Once installed, you can start the Redis server with:
```
redis-server
```

### Step 3: Set Up a Virtual Environment
1. **Create a Virtual Environment**
   ```
   python -m venv venv
   ```

2. **Activate the Virtual Environment**  
   **macOS/Linux**:
     ```
     source venv/bin/activate
     ```

3. **Install Dependencies**
   ```
   pip install Flask requests redis python-dotenv flask-limiter
   ```

### Step 4: Set up environment variables
Create a .env file in the project root and add the following keys:
```
WEATHER_API_KEY=your_visual_crossing_api_key
REDIS_URL=redis://localhost:6379/0
```

## Usage
1. Run the Flask app:
   ```
   python app.py
   ```

2. The app will run on `http://127.0.0.1:5000/` by default.

3. You can test the API using curl, Postman, or any HTTP client.  
   Example:
   ```
   curl "http://127.0.0.1:5000/weather?city=London"
   ```
