INSERT INTO dimUniversities 
    (university_name,delivery_method, founded,affiliation,university_link)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (university_name)
DO UPDATE
SET 
  founded = EXCLUDED.founded,
  affiliation = EXCLUDED.affiliation,
  delivery_method = EXCLUDED.delivery_method,
  university_link = EXCLUDED.university_link;
