from dotenv import load_dotenv 
import os
from peewee import *
import uuid
load_dotenv()

database = DatabaseProxy()

TEST_DB = SqliteDatabase(':memory:')

PG_DB = PostgresqlDatabase(
    os.getenv('DB_NAME'), 
    user=os.getenv('DB_USERNAME'), 
    host=os.getenv('DB_HOST'), 
    password=os.getenv('DB_PASSWORD'), 
    port=os.getenv('DB_PORT'))

def connect_to_db(app, db):
    try:
        database.initialize(db)
        database.connect(reuse_if_open=True)
    except OperationalError as e:
        app.logger.error(f'DB connection error: {e}')
        database.close()
        raise
        

class BaseModel(Model):
    class Meta:
        database = database

class Coin(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(80, unique = True)
    description = CharField(255)
    class Meta:
        table_name='coins'

