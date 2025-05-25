CREATE TABLE IF NOT EXISTS universities(
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

CREATE TABLE IF NOT EXISTS dimUniversities(
    university_id SERIAL PRIMARY KEY,
    university_name VARCHAR(255) NOT NULL,

    founded INT NOT NULL,
    university_link VARCHAR(300) NOT NULL,

    UNIQUE (university_name)
);

CREATE TABLE IF NOT EXISTS dimLocations(
    location_id SERIAL PRIMARY KEY,
    location_city VARCHAR(50) NOT NULL,
    location_country VARCHAR(50) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    
    UNIQUE (location_city,location_country,continent)
);

CREATE TABLE IF NOT EXISTS dimAffilations(
    affiliation_id SERIAL PRIMARY KEY,
    affiliation VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS dimDeliveryMethods(
    delivery_method_id SERIAL PRIMARY KEY,
    delivery_method VARCHAR(255) NOT NULL
);

CREATE TABLE  IF NOT EXISTS factRankings(
      id SERIAL PRIMARY KEY,
      university_rank INT NOT NULL,
      enrollment BIGINT NOT NULL,
      university_id INT NOT NULL,
      location_id INT NOT NULL,
      updated_year INT NOT NULL,
      delivery_method_id INT NOT NULL,
      affiliation_id INT NOT NULL,
    

    FOREIGN KEY (university_id) REFERENCES dimUniversities(university_id),
    FOREIGN KEY (delivery_method_id) REFERENCES dimDeliveryMethods(delivery_method_id),
    FOREIGN KEY (affiliation_id) REFERENCES dimAffilations(affiliation_id),
    FOREIGN KEY (location_id) REFERENCES dimLocations(location_id)
);

