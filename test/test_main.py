from pg8000 import Connection, InterfaceError, DatabaseError
from src.main import get_connection, get_data
import datetime
import pytest

connection_params = {
    "user": "myuser",
    "password": "mypassword",
    "database": "mydatabase",
    "host": "localhost",
    "port": 5433,
}


def test_get_connection():
    test_conn = get_connection(connection_params)
    results = test_conn.run("SELECT * FROM employees LIMIT 1")
    test_conn.close()
    assert results == ([1, "John", "Smith", datetime.date(2023, 11, 11)],)


def test_insert_values_into_psql():
    test_conn = get_connection(connection_params)
    test_conn.run(
        "INSERT INTO employees (first_name, last_name, started_date) VALUES ('A', 'B', '2100-05-10');"
    )
    test_conn.commit()

    results = test_conn.run("SELECT * FROM employees;")
    assert results == (
        [1, "John", "Smith", datetime.date(2023, 11, 11)],
        [2, "Harry", "Potter", datetime.date(2022, 10, 12)],
        [3, "Boris", "Johnson", datetime.date(2050, 5, 10)],
        [4, "A", "B", datetime.date(2100, 5, 10)],
    )


# def test_error_invalid_credentials():
#     connection_params_wrong = {"user": "user"}
#     with pytest.raises(InterfaceError):
#         conn = get_connection(connection_params_wrong)
#         get_data(conn)
