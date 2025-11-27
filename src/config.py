from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

env = load_dotenv()

# Connection string - configure your database connection here
schema = "liane_library"
host = "127.0.0.1" 
user = "root"
password = os.getenv("DB_PASSWORD")
port = 3306

connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

# Create SQLAlchemy engine
engine = create_engine(connection_string)
