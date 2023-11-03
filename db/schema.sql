DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_id serial PRIMARY KEY,
    first_name VARCHAR (50),
    last_name VARCHAR (50),
    started_date DATE
);