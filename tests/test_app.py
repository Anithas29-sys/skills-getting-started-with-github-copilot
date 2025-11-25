import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test POST /activities/{activity_name}/signup
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
])
def test_signup_for_activity(activity, email):
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400

# Test DELETE /activities/{activity_name}/participant
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
])
def test_remove_participant(activity, email):
    # Remove participant
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try removing again (should fail)
    response2 = client.delete(f"/activities/{activity}/participant?email={email}")
    assert response2.status_code == 404

# Test invalid activity
def test_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    response2 = client.delete("/activities/Nonexistent/participant?email=test@mergington.edu")
    assert response2.status_code == 404
