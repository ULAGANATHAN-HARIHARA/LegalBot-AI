import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="judibot",
        password="judipass",
        database="judiciary_ai"
    )
    print("✅ Connected successfully!")
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
