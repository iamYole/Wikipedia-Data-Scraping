CREATE TABLE universities(
    id BIGINT AUTO_INCREMENT NOT NULL,
    university_rank INT NOT NULL,
    university_name VARCHAR(255) NOT NULL,
    delivery_method VARCHAR(255) NOT NULL,
    enrollment BIGINT NOT NULL,
    founded INT NOT NULL,
    affiliation VARCHAR(50) NOT NULL,
    location_city VARCHAR(50) NOT NULL,
    location_country VARCHAR(50) NOT NULL,
    continent VARCHAR(50) NOT NULL,
    `location` VARCHAR(255) NOT NULL,
    `link` VARCHAR(300) NOT NULL,

    UNIQUE KEY unique_combination(`location_country`, `university_name`),
    PRIMARY KEY (id)
)
