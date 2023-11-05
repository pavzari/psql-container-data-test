import subprocess
import pytest
import time
import datetime
import pg8000
import os

test_dir = os.path.dirname(os.path.abspath(__file__))
compose_path = os.path.join(test_dir, "..", "docker-compose.yaml")


@pytest.fixture(scope="module")
def pg_container_conn():
    subprocess.run(["docker", "compose", "-f", compose_path, "up", "-d"])
    try:
        max_attempts = 5
        for _ in range(max_attempts):
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    "postgres",
                    "pg_isready",
                    "-h",
                    "localhost",
                    "-U",
                    "totesys",
                ],
                stdout=subprocess.PIPE,
            )
            if result.returncode == 0:
                break
            time.sleep(2)
        else:
            raise TimeoutError(
                "PostgreSQL container is not responding, cancelling fixture setup."
            )
        conn = pg8000.connect(
            host="localhost",
            user="totesys",
            password="totesys",
            database="totesys",
        )
        yield conn
    finally:
        conn.close()
        subprocess.run(["docker", "compose", "-f", compose_path, "down"])


@pytest.fixture(scope="module")
def pg_container():
    subprocess.run(["docker", "compose", "-f", compose_path, "up", "-d"])
    # subprocess.run(f"docker compose -f {compose_path} up -d", shell=True)
    try:
        max_attempts = 5
        for _ in range(max_attempts):
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    "postgres",
                    "pg_isready",
                    "-h",
                    "localhost",
                    "-U",
                    "totesys",
                ],
                stdout=subprocess.PIPE,
            )
            # result = subprocess.run(
            #     f"docker exec postgres pg_isready -h localhost -U totesys",
            #     shell=True,
            #     stdout=subprocess.PIPE,
            # )
            if result.returncode == 0:
                break
            time.sleep(2)
        else:
            raise TimeoutError(
                "PostgreSQL container is not responding, cancelling fixture setup."
            )
        yield
    finally:
        subprocess.run(["docker", "compose", "-f", compose_path, "down"])
        # subprocess.run(f"docker compose -f {compose_path} down", shell=True)


def test_db_connection(pg_container):
    conn = pg8000.connect(
        user="totesys",
        password="totesys",
        host="localhost",
        port=5433,
        database="totesys",
    )
    cursor = conn.cursor()
    # cursor.execute("SELECT 1 + 1")
    cursor.execute("SELECT * from employees limit 1;")
    result = cursor.fetchone()  # [0]
    assert result == ([1, "John", "Smith", datetime.date(2023, 11, 11)])


def test_returns_table_with_new_insertion(pg_container):
    conn = pg8000.connect(
        user="totesys",
        password="totesys",
        host="localhost",
        port=5433,
        database="totesys",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * from employees;")
    result = cursor.fetchall()
    assert result == (
        [1, "John", "Smith", datetime.date(2023, 11, 11)],
        [2, "Harry", "Potter", datetime.date(2022, 10, 12)],
        [3, "Boris", "Johnson", datetime.date(2050, 5, 10)],
    )
    cursor.execute(
        "INSERT INTO employees (first_name, last_name, started_date) VALUES ('A', 'B', '2100-05-10');"
    )
    cursor.execute("SELECT * from employees;")
    result = cursor.fetchall()
    assert result == (
        [1, "John", "Smith", datetime.date(2023, 11, 11)],
        [2, "Harry", "Potter", datetime.date(2022, 10, 12)],
        [3, "Boris", "Johnson", datetime.date(2050, 5, 10)],
        [4, "A", "B", datetime.date(2100, 5, 10)],
    )
