from pg8000 import Connection, InterfaceError, DatabaseError


def get_connection():
    conn = Connection(
        user="myuser",
        password="mypassword",
        database="mydatabase",
        host="localhost",
        port=5433,
        # for both runner and postgres in the same network:
        # host="postgres",
        # port = 5433
    )
    return conn


def get_data(conn):
    try:
        results = conn.run("SELECT * FROM employees")
        for row in results:
            print(row)
    except (InterfaceError, DatabaseError) as e:
        print(f"There was a database error: {e}")
    except Exception as e:
        print(f"There was an unexpected error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    conn = get_connection()
    get_data(conn)
