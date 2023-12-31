CREATE DATABASE IF NOT EXISTS HeadHunter
CREATE TABLE IF NOT EXISTS HH_vacancies
(id SERIAL PRIMARY KEY,
 company_id INTEGER,
 vacancy VARCHAR,
 salary_min INTEGER,
 description TEXT,
 url VARCHAR)


CREATE TABLE IF NOT EXISTS HH_employers
(company_id INTEGER PRIMARY KEY,
 company_name VARCHAR,
 open_vacancies INTEGER,
 url VARCHAR)