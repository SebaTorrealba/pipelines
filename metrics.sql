USE weather_db;

#Average observed temperature for last week(Mon-Sun).
SELECT AVG(temperature) AS avg_temperature
FROM weather_data
WHERE observation_timestamp >= NOW() - INTERVAL 7 DAY;

#Maximum wind speed change between two consecutive observations in the last 7 days.
SELECT MAX(ABS(wind_speed_dif)) as max_wind_speed_dif
FROM (
SELECT	observation_timestamp,
		wind_speed,
        wind_speed - LAG(wind_speed)
        OVER(ORDER BY observation_timestamp) AS wind_speed_dif
FROM	weather_data
WHERE	observation_timestamp >= NOW() - INTERVAL 7 DAY) AS a
ORDER BY ABS(wind_speed_dif) DESC