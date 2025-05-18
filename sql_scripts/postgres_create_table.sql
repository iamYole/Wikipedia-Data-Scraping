CREATE TABLE universities(
    id SERIAL PRIMARY KEY,
    university_rank INT NOT NULL,
    university_name VARCHAR(255) NOT NULL,
    delivery_method VARCHAR(255) NOT NULL,
    enrollment BIGINT NOT NULL,
    founded INT NOT NULL,
    affiliation VARCHAR(50) NOT NULL,
    location_city VARCHAR(50) NOT NULL,
    location_country VARCHAR(50) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    uni_location VARCHAR(255) NOT NULL,
    uni_link VARCHAR(300) NOT NULL,
    updated_year INT NOT NULL,


    UNIQUE (location_country, university_name, updated_year)
);

CREATE TABLE dimUniversities(
    university_id SERIAL PRIMARY KEY,
    university_name VARCHAR(255) NOT NULL,
    delivery_method VARCHAR(255) NOT NULL,
    founded INT NOT NULL,
    affiliation VARCHAR(50) NOT NULL,
    university_link VARCHAR(300) NOT NULL,

    UNIQUE (university_name)
);

CREATE TABLE dimLocation(
    location_id SERIAL PRIMARY KEY,
    location_city VARCHAR(50) NOT NULL,
    location_country VARCHAR(50) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    
    UNIQUE (location_city,location_country,continent)
);

CREATE TABLE factRankings(
      id SERIAL PRIMARY KEY,
      university_rank INT NOT NULL,
      enrollment BIGINT NOT NULL,
      university_id INT NOT NULL,
      location_id INT NOT NULL,
      updated_year INT NOT NULL,
    

    FOREIGN KEY (university_id) REFERENCES dimUniversities(university_id),
    FOREIGN KEY (location_id) REFERENCES dimLocation(location_id)
);

