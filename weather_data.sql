CREATE TABLE `weather_data` (
  `station_id` varchar(10) NOT NULL,
  `station_name` varchar(100) DEFAULT NULL,
  `station_timezone` varchar(50) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `observation_timestamp` datetime NOT NULL,
  `temperature` decimal(5,2) DEFAULT NULL,
  `wind_speed` decimal(5,2) DEFAULT NULL,
  `humidity` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`station_id`,`observation_timestamp`)
);