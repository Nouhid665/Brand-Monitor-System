import sqlite3

DB_NAME = "brand_monitor.db"

#  CREATE DATABASE & TABLE
def create_db():
    conn = sqlite3.connect(DB_NAME)#Creates a file called brand_monitor.db if it doesn't exist
    cursor = conn.cursor()# cursor lets you execute SQL commands on the database.

    #Creating the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mentions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            brand       TEXT,
            source      TEXT,
            title       TEXT,
            content     TEXT,
            url         TEXT,
            sentiment   TEXT,
            score       REAL,
            fetched_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit() #permanently saves the table creation
    conn.close() #Closes the database connection to free resources.
    print("Database ready.")


#INSERT ONE MENTION 
def insert_mention(brand, source, title, content, url, sentiment, score):

    # DATABASE CONNECTION
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # check if this url already exists for this brand
    cursor.execute("SELECT id FROM mentions WHERE brand = ? AND url = ?", (brand, url))
    existing = cursor.fetchone()
    
    if existing:
        conn.close()
        return 

    cursor.execute("""
        INSERT INTO mentions (brand, source, title, content, url, sentiment, score)
        VALUES (?, ?, ?, ?, ?, ?, ?) -- "?"this are the placeholder in which the inserted value will be added
    """, (brand, source, title, content, url, sentiment, score))
    # save the changes 
    conn.commit()
    # close the database
    conn.close()


# GET ALL MENTIONS FOR A BRAND
def get_mentions(brand):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM mentions
        WHERE LOWER(brand) = LOWER(?)
        ORDER BY fetched_at DESC
    """, (brand,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]