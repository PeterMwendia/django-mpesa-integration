import sqlite3
import psycopg2

from django.conf import settings

def create_table(table_name, columns):
    if settings.DEBUG:
        # Use SQLite3
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
    else:
        # Use PostgreSQL
        conn = psycopg2.connect(
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        c = conn.cursor()

    columns_str = ', '.join(columns)
    c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def populate_table(table_name, data):
    if settings.DEBUG:
        # Use SQLite3
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
    else:
        # Use PostgreSQL
        conn = psycopg2.connect(
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        c = conn.cursor()

    for row in data:
        placeholders = ', '.join(['%s'] * len(row))
        c.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
