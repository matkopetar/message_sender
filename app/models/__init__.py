import databases
from sqlalchemy import MetaData, create_engine

from app.utils.constants import DATABASE_URL

database = databases.Database(DATABASE_URL)
metadata = MetaData()

from app.models.message import messages  # noqa

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata.create_all(engine)
