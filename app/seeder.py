from app.db import *
from app.app import app

def seed_data():
    connect_to_db(app)
    database.drop_tables([Coin, Duty, CoinDuty, RequestLog])
    database.create_tables([Coin, Duty, CoinDuty, RequestLog])

    Coin.create(name='automate', description='automation')
    Coin.create(name='Security', description='secure the bag')
    assemble = Coin.create(name='assemble', description='assemble the team')

    Duty.create(name='D1', description='duty 1')
    Duty.create(name='D2', description='duty 2')
    duty_4 = Duty.create(name='D4', description='duty 4')
    
    CoinDuty.create(coin=assemble, duty=duty_4)
    database.close()

seed_data()
