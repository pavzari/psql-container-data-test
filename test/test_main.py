from src.main import get_connection
import datetime


def test_get_connection():
    test_conn = get_connection()
    results = test_conn.run("SELECT * FROM employees LIMIT 1")
    assert results == ([1, "John", "Smith", datetime.date(2023, 11, 11)],)
