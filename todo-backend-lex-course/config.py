import os

# Database location
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(r"C:\DB'S", 'app.db')
# print("base", DATABASE_URI)
# Path to SQLite database file