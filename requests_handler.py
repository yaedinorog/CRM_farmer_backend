import sqlite3 
from db_handler import create_connection

def add_request(name, good, category, cost, farmer_id=1):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    insert into requests (name, goods, category, cost, farmer_id) values (?, ?, ?, ?, ?)
''', (name, good, category, cost, farmer_id))
    conn.commit()
    cursor.close()
    print("Request added successfully.")

def get_requests():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select * from requests
''')
    requests = cursor.fetchall()
    cursor.close()
    return requests

def update_request(id, name, good, category, cost):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    update requests set name = ?, goods = ?, category = ?, cost = ? where id = ?
''', (name, good, category, cost, id))
    conn.commit()
    cursor.close()
    print("Request updated successfully.")

def delete_request(id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    delete from requests where ID = ?
''', (id,))
    conn.commit()
    cursor.close()
    print("Request deleted successfully.")

def get_requests_by_farmer(farmer_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select * from requests where farmer_id = ?
''', (farmer_id,))
    requests = cursor.fetchall()
    cursor.close()
    return requests