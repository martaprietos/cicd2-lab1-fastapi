import pytest

def user_payload(
    name="Paul",
    email="paul@atu.ie",
    age=25,
    student_id="S1234567",
):
    return {
        "name": name,
        "email" : email,
        "age" : age,
        "student_id" : student_id,
    }

def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Paul"

def test_create_user_with_existing_user_id_returns_409(client):
    client.post("/api/users", json=user_payload())

    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()

@pytest.mark.parametrize("bad_student_id", ["1234567",  "s1234567",  "S123", "S12345678"],
)
def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post(
        "/api/users",
        json=user_payload(student_id=bad_student_id),
    )
    assert response.status_code == 422

def test_get_users_returns_created_users(client):
    created = client.post("/api/users", json=user_payload()).json()

    user_id = created["id"]
    response = client.get("/api/users")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "paul@atu.ie"

def test_get_existing_user_returns_200(client):
    created = client.post("/api/users",json=user_payload()).json()

    user_id = created["id"]
    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "paul@atu.ie"

def test_get_missing_user_returns_404(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_delete_existing_user_returns_204(client):
    created = client.post("/api/users", json=user_payload()).json()
    user_id = created["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

def test_delete_missing_user_returns_404(client):
    response = client.delete("/api/users/999")
    
    assert response.status_code == 404

def test_deleted_user_can_no_longer_be_retrieved(client):
    created = client.post("/api/users", json=user_payload()).json()
    user_id = created["id"]
    client.delete(f"/api/users/{user_id}")
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 404