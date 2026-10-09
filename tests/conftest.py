import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import get_db
from app.main import app
from app.models import BASE
TEST_DATABASE_URL = "sqlite+pysqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db #call override db instead of the original get_db function

@pytest.fixture(autouse=True)
def reset_database(): #every test we need a clean db
    BASE.metadata.create_all(bind=test_engine)#create to test engine
    yield
    BASE.metadata.drop_all(bind=test_engine)#drop to test engine
@pytest.fixture
def client():
    return TestClient(app)
