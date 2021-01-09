from sqlalchemy import Table, Column, Integer, String, Float, MetaData, create_engine, update
from sqlalchemy_utils import database_exists, create_database
import os

db_path = os.path.join(os.path.dirname(__file__), 'main.db')
db_url = 'sqlite:///{}'.format(db_path)

# Create engine (connection)
engine = create_engine(db_url, echo=True)

# Create database file
if not database_exists(engine.url):
    create_database(engine.url)

# Create table
metadata = MetaData()
last_message = Table('last_message', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('last_run', Integer, nullable=False)
                     )
settings = Table('settings', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('count_days', Integer, nullable=False),
                 Column('caption', String(1024), nullable=False),
                 Column('messages', String(10000), nullable=False),
                 Column('time_start', Float, nullable=False)
                 )

# Execute "Create tables"
metadata.create_all(engine)


# Connect to DB
conn = engine.connect()


def check_first_run():
    temp = len(list(conn.execute(last_message.select())))
    if temp < 1:
        conn.execute(last_message.insert().values(last_run=0))
    elif temp > 1:
        conn.execute(last_message.delete().where(last_message.c.id != 1))

    temp = len(list(conn.execute(settings.select())))
    if temp < 1:
        conn.execute(settings.insert().values(count_days=1, caption='', messages='', time_start=00.01))
    elif temp > 1:
        conn.execute(settings.delete().where(settings.c.id != 1))


def get_last_message():
    for row in conn.execute(last_message.select()):
        return row


def get_settings():
    for row in conn.execute(settings.select()):
        return row


def edit_last_message(last_run):
    conn.execute(last_message.update(last_message).where(last_message.c.id == 1).values(last_run=last_run))


def edit_settings(count_days, caption, messages, time_start):
    conn.execute(settings.update(settings).where(settings.c.id == 1).values(count_days=count_days, caption=caption, messages=messages, time_start=time_start))
