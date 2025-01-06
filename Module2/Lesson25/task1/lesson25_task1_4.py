"""Lesson25 Task1-4"""

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
        SELECT c.category_name, COUNT(p.product_id)
        FROM production.products AS p
        JOIN production.categories AS c ON p.category_id = c.category_id
        GROUP BY c.category_name;
        """
    )

    for record in cursor.fetchall():
        print(record)

except Error as e:
    print("Возникло исключение при работе с Postgres", e)
