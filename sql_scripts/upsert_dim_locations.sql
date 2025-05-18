INSERT INTO dimLocations 
    (location_city,location_country, continent)
VALUES (%s, %s, %s)
ON CONFLICT (location_city,location_country, continent)
DO UPDATE
SET
    location_city = EXCLUDED.location_city,
    location_country = EXCLUDED.location_country,
    continent = EXCLUDED.continent;

