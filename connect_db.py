from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Retrieve environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DIALECT = os.getenv('DB_DIALECT')

# Construct the DATABASE_URL
DATABASE_URL = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Print to verify the URL (optional)
print(f"DATABASE_URL: {DATABASE_URL}")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
