"""Lesson25 Task1-2"""

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
        SELECT st.first_name, st.last_name, s.store_name
        FROM sales.staffs AS st
        JOIN sales.stores AS s ON st.store_id = s.store_id
        WHERE st.active = 1;
        """
    )

    for record in cursor.fetchall():
        print(record)

except Error as e:
    print("Возникло исключение при работе с Postgres", e)
