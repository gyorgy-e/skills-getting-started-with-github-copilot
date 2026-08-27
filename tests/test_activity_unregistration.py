from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_activity_data():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]
    assert "schedule" in payload[expected_activity]


def test_signup_for_activity_adds_new_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_missing_participant_returns_404():
    # Arrange
    activity_name = "Art Club"
    email = "ghost@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={quote(email)}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
