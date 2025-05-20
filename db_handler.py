import sqlite3

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_base_schema():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        create table if not exists users (
        id integer primary key autoincrement,
        username text not null,
        password_hash text not null)
                   ''')
    cursor.execute('''
        create table if not exists farmers (
        id integer primary key autoincrement,
        name text not null,
        surname text,
        patr text not null
        )
                   ''')
    cursor.execute('''
        create table if not exists production (
        id integer primary key autoincrement,
        name text not null,
        quality integer not null,
        amount integer not null,
        price integer not null,
        farmer_id integer not null
        references farmers(id)
        )
                   ''')
    cursor.execute('''
        create table if not exists requests (
        id integer primary key autoincrement,
        name text not null, 
        goods text not null,
        category text not null,
        cost int not null,
        farmer_id integer not null references farmers(id))
''')

    conn.commit()
    cursor.close()
    print("Base schema created successfully.")


if __name__ == "__main__":
    create_base_schema()