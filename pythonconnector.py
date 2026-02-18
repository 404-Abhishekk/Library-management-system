import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="8590488141",   # your mysql password
    database="LibraryDB"
)

if db.is_connected():
    print("connected successfully")

cursor = db.cursor()

# 1. Fetch Books
print(" Books Table")
cursor.execute("SELECT * FROM Book")
for row in cursor.fetchall():
    print(row)

print("\n------------------\n")

# 2. Fetch Members
print( "Members Table")
cursor.execute("SELECT * FROM Members")
for row in cursor.fetchall():
    print(row)

print("\n------------------\n")

# 3. Fetch Transactions
print("Librarian Table")
cursor.execute("SELECT * FROM Librarian")
for row in cursor.fetchall():
    print(row)

cursor.close()
db.close()