import psycopg2
from pathlib import Path
import csv

conn = psycopg2.connect(
    dbname='python-rec-db',
    user='postgres',
    host='localhost',
    port='5433',
    password='1234'
)
cur = conn.cursor()

file_path_1 = Path("/home/artem/python_MAI_project/project/reccomendation_api/Kek/items.csv")
file_path_2 = Path("/home/artem/python_MAI_project/project/reccomendation_api/Kek/item_categories.csv")

create_table_qquery_1 = """
CREATE TABLE IF NOT EXISTS items (
    item_name TEXT,
    item_id SERIAL PRIMARY KEY,
    item_category_id BIGINT 
);
"""

create_table_qquery_2 = """
CREATE TABLE IF NOT EXISTS categories (
    item_category_id SERIAL PRIMARY KEY,
    item_category_name TEXT
    
);
"""


cur.execute(create_table_qquery_2)
cur.execute(create_table_qquery_1)
conn.commit()

with file_path_2.open(newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        cur.execute("""
            INSERT INTO categories (item_category_name)
            VALUES (%s)
            ON CONFLICT (item_category_id) DO UPDATE SET
                    item_category_id = EXCLUDED.item_category_id
        """, (row[0],))
conn.commit()

with file_path_1.open(newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    for row in reader:
        cur.execute("""
            INSERT INTO items (item_name, item_category_id)
            VALUES (%s, %s)
            ON CONFLICT (item_id) DO UPDATE SET
                    item_name = EXCLUDED.item_name,
                    item_category_id = EXCLUDED.item_category_id
        """, (row[0],row[2]))
conn.commit()

join_query = """
SELECT i.item_name, i.item_id, c.item_category_name
FROM items i
JOIN categories c ON i.item_category_id = c.item_category_id;
"""

cur.execute(join_query)
rows = cur.fetchall()

# for row in rows:
#     print(row)

cur.close()
conn.close()