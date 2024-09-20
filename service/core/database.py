from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

def get_db_connection():
    engine = create_engine(
        f"postgresql+psycopg2://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )
    Session = sessionmaker(bind=engine)
    return Session
