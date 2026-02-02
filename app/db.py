from dotenv import load_dotenv 
import os
from peewee import *
import uuid

load_dotenv()

database = DatabaseProxy()

TEST_DB = SqliteDatabase(":memory:")

PG_DB = PostgresqlDatabase(
        os.getenv('DB_NAME'), 
        user=os.getenv('DB_USERNAME'), 
        host=os.getenv('DB_HOST'), 
        password=os.getenv('DB_PASSWORD'), 
        port=os.getenv('DB_PORT'),
        sslmode='require'
    )
        

ENV = os.getenv("FLASK_ENV", "production").lower()

if ENV == "test":
    database.initialize(TEST_DB)
else:
    database.initialize(PG_DB)

def connect_to_db(app):
    try:
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

class Duty(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(80, unique = True)
    description = CharField(255)
    class Meta:
        table_name='duties'

class CoinDuty(BaseModel):
    coin = ForeignKeyField(Coin, backref='coin_duties', on_delete='CASCADE')
    duty = ForeignKeyField(Duty, backref='coin_duties', on_delete='CASCADE')
    class Meta:
        table_name='coin_duties'
        primary_key = CompositeKey('coin', 'duty')
