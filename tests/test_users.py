import pytest

from tests.conftest import client

def user_payload(
    uid=1,
    name="Paul",
    email="paul@atu.ie",
    age=25,
    student_id="S1234567",
):
    return {
        "user_id" : uid,
        "name": name,
        "email" : email,
        "age" : age,
        "student_id" : student_id,
    }

def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["name"] == "Paul"
    assert data["email"] == "paul@atu.ie"

def test_create_user_with_existing_user_id_returns_409(client):
    client.post("/api/users", json=user_payload(uid=2))

    response = client.post("/api/users", json=user_payload(uid=2))

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()

@pytest.mark.parametrize("bad_student_id", ["1234567",  "s1234567",  "S123", "S12345678"],
)
def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post(
        "/api/users",
        json=user_payload(uid=3, student_id=bad_student_id),
    )
    assert response.status_code == 422