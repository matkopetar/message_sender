import os
import databases
from sqlalchemy import MetaData, create_engine


database = databases.Database(os.environ.get('DATABASE_URL'))
metadata = MetaData()

from app.models.message import messages  # noqa

engine = create_engine(os.environ.get('DATABASE_URL'), connect_args={'check_same_thread': False})
metadata.create_all(engine)
