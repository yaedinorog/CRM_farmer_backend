import sqlite3
from db_handler import create_connection

def add_farmer(name, surname, patr):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    insert into farmers (name, surname, patr) values (?, ?, ?)
''', (name, surname, patr))
    conn.commit()
    cursor.close()
    print("Farmer added successfully.")

def get_farmers():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    with base as (select farmers.id, 
                   farmers.name, 
                   farmers.surname, 
                   farmers.patr, 
                   sum(requests.cost) as total_credit, 
                   sum(production.price) as total_earnings  
                from farmers
    join production on farmers.id = production.farmer_id
    join requests on farmers.id = requests.farmer_id
    group by farmers.id, farmers.name, farmers.surname, farmers.patr)

    select *, total_earnings - total_credit as balance from base    
    ''')
    farmers = cursor.fetchall()
    cursor.close()
    return farmers

def update_farmer(id, name, surname, patr):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    update farmers set name = ?, surname = ?, patr = ? where id = ?
''', (name, surname, patr, id))
    conn.commit()
    cursor.close()
    print("Farmer updated successfully.")

def delete_farmer(id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    delete from farmers where ID = ?
''', (id,))
    conn.commit()
    cursor.close()
    print("Farmer deleted successfully.")

def get_farmer_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select * from farmers where id = ?
''', (id,))
    farmer = cursor.fetchone()
    cursor.close()
    return farmer