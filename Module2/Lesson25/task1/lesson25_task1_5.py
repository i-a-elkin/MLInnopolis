"""Lesson25 Task1-5"""

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
        SELECT c.first_name, c.last_name, COUNT(o.order_id)
        FROM sales.customers AS c
        -- Используем LEFT JOIN, чтобы включить клиентов без заказов
        LEFT JOIN sales.orders AS o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id
        ORDER BY c.first_name,  c.last_name;        
        """
    )

    for record in cursor.fetchall():
        print(record)

except Error as e:
    print("Возникло исключение при работе с Postgres", e)
