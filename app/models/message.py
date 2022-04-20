from sqlalchemy import Column, Table, Integer, String

from app.models import metadata


messages = Table(
    'messages',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String),
    Column('client_id', Integer),
)
