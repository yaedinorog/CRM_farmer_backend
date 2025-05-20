import sqlite3
from db_handler import create_connection
import jwt
import datetime
from dotenv import load_dotenv
import os

def Register (Username, Password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select * from users where username = ?
    ''', (Username,))
    if cursor.fetchone():
        cursor.close()
        return False

    conn.execute('''
    insert into users (username, password_hash) values (?, ?)
''', (Username, Password))
    conn.commit()
    cursor.close()
    return True

def Login (Username, Password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    select * from users where username = ? and password_hash = ?
''', (Username, Password))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return True
    else:
        return False
    
def create_access_token(data):
    load_dotenv()
    secret_key = os.getenv("SECRET_JWT_KEY")
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    token = jwt.encode({"data": data, "exp": expiration}, secret_key, algorithm="HS256")
    return token

def verify_access_token(token):
    load_dotenv()
    secret_key = os.getenv("SECRET_JWT_KEY")
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

if __name__ == "__main__":
    Register("test", "test")
    print(Login("test", "test"))
    print(verify_access_token(create_access_token({"sub":"test"})))