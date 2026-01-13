from dotenv import load_dotenv 
import os
from peewee import *
load_dotenv()

postgres_db = PostgresqlDatabase(
    os.getenv('DB_NAME'), 
    user=os.getenv('DB_USERNAME'), 
    host=os.getenv('DB_HOST'), 
    password=os.getenv('DB_PASSWORD'), 
    port=os.getenv('DB_PORT'))

def connect_to_db(app):
    try:
        postgres_db.connect(reuse_if_open=True)
        print('db connection successful')
    except OperationalError as e:
        app.logger.error(f'DB connection error: {e}')
        raise

class BaseModel(Model):
    class Meta:
        database = postgres_db
