"""Lesson25 Task1-1"""

import psycopg2
from psycopg2 import Error


try:
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="999999999",
        host="127.0.0.1",
        port="5432",
        options="-c client_encoding=utf8",
    )
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT p.product_name, b.brand_name
        FROM production.products AS p
        JOIN production.brands AS b ON p.brand_id = b.brand_id;
        """
    )

    for record in cursor.fetchall():
        print(record)

except Error as e:
    print("Возникло исключение при работе с Postgres", e)
