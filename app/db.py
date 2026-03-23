from dotenv import load_dotenv 
import os
from peewee import *
import uuid
import bcrypt

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


def connect_to_db(app):
    env = os.getenv("FLASK_ENV", "production").lower()
    db = TEST_DB if env == "test" else PG_DB
    database.initialize(db)

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
    name = CharField(35, unique = True)
    description = CharField(255)
    complete = BooleanField(default=False)
    class Meta:
        table_name='coins'

class Duty(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(3, unique = True)
    description = CharField(255)
    class Meta:
        table_name='duties'

class CoinDuty(BaseModel):
    coin = ForeignKeyField(Coin, backref='coin_duties', on_delete='CASCADE')
    duty = ForeignKeyField(Duty, backref='coin_duties', on_delete='CASCADE')
    class Meta:
        table_name='coin_duties'
        primary_key = CompositeKey('coin', 'duty')

class RequestLog(BaseModel):
    method = CharField()
    path = CharField()
    timestamp = DateTimeField()
    status_code = IntegerField()
    class Meta:
        table_name='request_logs'

class User(BaseModel):
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLES = (ROLE_USER, ROLE_ADMIN)

    id = UUIDField(primary_key=True, default=uuid.uuid4)
    username = CharField(80, unique=True)
    password_hash = CharField(200)
    role = CharField(10, default=ROLE_USER)

    class Meta:
            table_name = "users"

    def set_password(self, plain: str) -> None:
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(plain.encode(), salt).decode()

    def check_password(self, plain: str) -> bool:
        return bcrypt.checkpw(plain.encode(), self.password_hash.encode())
 
    @property
    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN    