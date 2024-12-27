import psycopg2
from pathlib import Path
import csv
import random
from datetime import datetime

conn = psycopg2.connect(
    dbname='python-back-db',
    user='postgres',
    host='localhost',
    port='5432',
    password='1234'
)
cur = conn.cursor()

file_path_1 = Path("kek/items.csv")
file_path_2 = Path("kek/item_categories.csv")





with file_path_2.open(newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    
    for row in reader:
        
        cur.execute("""
            INSERT INTO categories (name)
            VALUES (%s)
            ON CONFLICT (id) DO UPDATE SET
                    id = EXCLUDED.id
        """, (row[0],))
conn.commit()

with file_path_1.open(newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)
    k =0
    for row in reader:
        k += 1
        if k == 10000:
            break
        cur.execute("""
            INSERT INTO products (title, description, price, discount_percentage, stock, brand, images, created_at,category_id)
            VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    category_id = EXCLUDED.category_id
        """, (row[0],"Lorem Ipsum",random.randint(5,10000),0,random.randint(1,100),"Lorem",["image"],datetime.now().isoformat() ,row[2]))
conn.commit()



# cur.execute(join_query)
# rows = cur.fetchall()

# for row in rows:
#     print(row)

cur.close()
conn.close()