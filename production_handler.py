import sqlite3
from db_handler import create_connection

def add_production(name, quality, amount, price, farmer_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    insert into production (name, quality, amount, price, farmer_id) values (?, ?, ?, ?, ?)
''', (name, quality, amount, price, farmer_id))
    conn.commit()
    cursor.close()
    print("Production added successfully.")

def get_production():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select * from production
''')
    production = cursor.fetchall()
    cursor.close()
    return production

def update_production(id, name, quality, amount, price):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    update production set name = ?, quality = ?, amount = ?, price = ? where id = ?
''', (name, quality, amount, price, id))
    conn.commit()
    cursor.close()
    print("Production updated successfully.")

def delete_production(id:int):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    delete from production where ID = ?
''', (id))
    conn.commit()
    cursor.close()
    print("Production deleted successfully.")

def get_production_by_farmer(farmer_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select * from production where farmer_id = ?
''', (farmer_id,))
    production = cursor.fetchall()
    cursor.close()
    return production

if __name__ == "__main__":
    add_production("test", "test", 10, 100, 1)
    print(get_production())
    update_production(1, "test_updated", "test_updated", 20, 200)
    print(get_production())
    delete_production(1)
    print(get_production())