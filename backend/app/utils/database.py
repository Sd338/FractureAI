import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_name="fractures.db"):
        """Initialize the database connection and create tables if they don't exist."""
        self.connection = self.create_connection(db_name)
        self.create_tables()

    def create_connection(self, db_file):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(f"Connected to database: {db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")
        return conn

    def create_tables(self):
        """Create the necessary tables in the database."""
        create_fractures_table = '''
        CREATE TABLE IF NOT EXISTS fractures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            detection_results TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''

        try:
            if self.connection is not None:
                self.connection.execute(create_fractures_table)
                print("Fractures table created successfully.")
            else:
                print("Error: Connection to database is not established.")
        except Error as e:
            print(f"Error creating table: {e}")

    def add_fracture(self, image_path, detection_results):
        """Insert a new fracture record into the database."""
        sql = '''INSERT INTO fractures (image_path, detection_results)
                 VALUES (?, ?);'''
        try:
            cur = self.connection.cursor()
            cur.execute(sql, (image_path, detection_results))
            self.connection.commit()
            print("Fracture added successfully.")
        except Error as e:
            print(f"Error adding fracture: {e}")

    def get_fractures(self):
        """Retrieve all fracture records from the database."""
        sql = '''SELECT * FROM fractures;'''
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            fractures = cur.fetchall()
            return fractures
        except Error as e:
            print(f"Error retrieving fractures: {e}")
            return []

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

# Example usage
if __name__ == "__main__":
    db = Database()
    # Add a sample fracture
    db.add_fracture("path/to/image.jpg", "Detected fracture at location X.")
    # Retrieve fractures
    fractures = db.get_fractures()
    print(fractures)
    db.close()
