import requests
import mysql.connector
from datetime import datetime, timedelta

# Database connection parameters
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'weather_db'

# Constants
STATION_ID = '0007W'
BASE_URL = 'https://api.weather.gov/stations'
OBSERVATIONS_URL = f'{BASE_URL}/{STATION_ID}/observations'

def fetch_station_metadata():
    """Fetch metadata for the station."""
    response = requests.get(f'{BASE_URL}/{STATION_ID}')
    response.raise_for_status()
    return response.json()

def fetch_observations(start_date, end_date):
    """Fetch weather observations between start_date and end_date."""
    params = {
        'start': start_date,
        'end': end_date
    }
    response = requests.get(OBSERVATIONS_URL, params=params)
    response.raise_for_status()
    return response.json()

def insert_weather_data(cursor, data):
    """Insert weather data into the database."""
    insert_query = """
    INSERT INTO weather_data (station_id, station_name, station_timezone, latitude, longitude,
                              observation_timestamp, temperature, wind_speed, humidity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        temperature = VALUES(temperature),
        wind_speed = VALUES(wind_speed),
        humidity = VALUES(humidity);
    """   
    for entry in data:
        properties = entry['station']['properties']
        coordinates = entry['station']['geometry']['coordinates']
        cursor.execute(insert_query, (
            properties['stationIdentifier'],
            properties['name'],
            properties['timeZone'],
            coordinates[0],
            coordinates[1],
            entry['timestamp'],
            entry['temperature']['value'],
            entry['windSpeed']['value'],
            entry['humidity']['value'],
        ))

def main():
    # Calculate date range for the last 7 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    # Fetch station metadata
    station_metadata = fetch_station_metadata()

    # Fetch weather observations
    observations = fetch_observations(start_date.isoformat() + 'Z', end_date.isoformat() + 'Z')

    # Prepare data for insertion
    weather_data = []
    for obs in observations['features']:
        weather_data.append({
            'station': station_metadata,
            'timestamp': obs['properties']['timestamp'],
            'temperature': obs['properties']['temperature'],
            'windSpeed': obs['properties']['windSpeed'],
            'humidity': obs['properties']['relativeHumidity']
        })

    # Database interaction
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    cursor = connection.cursor()
   
    try:
        insert_weather_data(cursor, weather_data)
        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main()
