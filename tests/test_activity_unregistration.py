from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_with_delete_signup_route():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    before = activities[activity_name]["participants"][:]
    assert email in before

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert "unregistered" in response.json()["message"].lower()

    activities[activity_name]["participants"] = before


def test_unregister_participant_with_unreg_route():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    before = activities[activity_name]["participants"][:]
    assert email in before

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert "unregistered" in response.json()["message"].lower()

    activities[activity_name]["participants"] = before


def test_unregister_missing_email_returns_404():
    activity_name = "Art Club"
    email = "ghost@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
