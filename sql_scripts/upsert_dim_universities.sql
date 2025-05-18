INSERT INTO dimUniversities 
    (university_name, founded,university_link)
VALUES (%s, %s, %s)
ON CONFLICT (university_name)
DO UPDATE
SET 
  founded = EXCLUDED.founded,
  university_link = EXCLUDED.university_link;
