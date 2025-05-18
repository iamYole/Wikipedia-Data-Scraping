INSERT INTO universities (
  university_rank, university_name, uni_location, continent, founded,
  affiliation, delivery_method, enrollment, uni_link,
  location_city, location_country, updated_year
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (university_name, location_country, updated_year)
DO UPDATE
SET 
  university_rank = EXCLUDED.university_rank,
  uni_location = EXCLUDED.uni_location,
  continent = EXCLUDED.continent,
  founded = EXCLUDED.founded,
  affiliation = EXCLUDED.affiliation,
  delivery_method = EXCLUDED.delivery_method,
  enrollment = EXCLUDED.enrollment,
  uni_link = EXCLUDED.uni_link,
  location_city = EXCLUDED.location_city;



