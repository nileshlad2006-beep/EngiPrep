from db import get_connection
from werkzeug.security import generate_password_hash

full_name = "System Administrator"
username = "admin"
email = "admin@engiprep.com"
password = "admin123"

hashed_password = generate_password_hash(password)

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT user_id
    FROM users
    WHERE username=%s OR email=%s
""", (username, email))

existing = cursor.fetchone()

if existing:
    print("Admin already exists.")
else:

    cursor.execute("""
        INSERT INTO users
        (full_name, username, email, password_hash, role)
        VALUES(%s, %s, %s, %s, %s)
    """, (
        full_name,
        username,
        email,
        hashed_password,
        "admin"
    ))

    conn.commit()

    print("Admin account created successfully.")

cursor.close()
conn.close()