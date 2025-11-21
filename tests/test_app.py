import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]


def test_unregister_from_activity():
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "abgemeldet" in response.json()["message"]
    # Try to unregister again
    response_dup = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_dup.status_code == 400
    assert "not registered" in response_dup.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup?email=foo@bar.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_activity_not_found():
    response = client.post("/activities/UnknownActivity/unregister?email=foo@bar.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
