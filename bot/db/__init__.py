import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# SQLAlchemy Engine
uri = os.environ["DB_URI"]
engine = create_engine(uri)

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
Session = sessionmaker(bind=engine)
