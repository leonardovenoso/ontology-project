import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
import models  # ensures all models are registered on Base.metadata

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()