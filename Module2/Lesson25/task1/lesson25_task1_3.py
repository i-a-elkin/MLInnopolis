"""Lesson25 Task1-3"""

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
        SELECT c.first_name, c.last_name, c.email, c.phone
        FROM sales.customers AS c
        JOIN sales.orders AS o ON c.customer_id = o.customer_id
        JOIN sales.stores AS s ON o.store_id = s.store_id
        WHERE s.store_name = 'Santa Cruz Bikes';
        """
    )

    for record in cursor.fetchall():
        print(record)

except Error as e:
    print("Возникло исключение при работе с Postgres", e)
