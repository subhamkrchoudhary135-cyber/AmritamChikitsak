"""Pytest fixtures for Sanjivani AI test suite."""

import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.core.database import Base, get_db
from src.core.security import UserRole, create_access_token, get_password_hash
from src.db.models import Patient, User
from src.main import app

# In-memory test SQLite async engine
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_sanjivani.db"

test_async_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a fresh database session per test function."""
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Test HTTP client with overridden database dependency."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_patient_user(db_session: AsyncSession) -> User:
    """Create a verified patient user and profile."""
    user = User(
        email="patient@example.com",
        username="patient_test",
        hashed_password=get_password_hash("SecretPassword123!"),
        role=UserRole.PATIENT.value,
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.flush()

    patient = Patient(
        user_id=user.id,
        full_name="Rajesh Sharma",
        phone_number="+919876543210",
        abha_id="91-1234-5678-9012",
        age=45,
        gender="male",
        preferred_language="en",
        state_province="Punjab",
    )
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_doctor_user(db_session: AsyncSession) -> User:
    """Create a verified doctor user."""
    doctor = User(
        email="doctor@example.com",
        username="dr_verma",
        hashed_password=get_password_hash("DoctorSecret123!"),
        role=UserRole.DOCTOR.value,
        is_active=True,
        is_verified=True,
    )
    db_session.add(doctor)
    await db_session.commit()
    await db_session.refresh(doctor)
    return doctor


@pytest.fixture
def patient_token(test_patient_user: User) -> str:
    """JWT bearer token for test patient."""
    return create_access_token(subject=test_patient_user.id, role=UserRole.PATIENT)


@pytest.fixture
def doctor_token(test_doctor_user: User) -> str:
    """JWT bearer token for test doctor."""
    return create_access_token(subject=test_doctor_user.id, role=UserRole.DOCTOR)


@pytest.fixture
def patient_headers(patient_token: str) -> dict:
    return {"Authorization": f"Bearer {patient_token}"}


@pytest.fixture
def doctor_headers(doctor_token: str) -> dict:
    return {"Authorization": f"Bearer {doctor_token}"}
