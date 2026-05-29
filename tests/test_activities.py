"""Tests for activities API endpoints using AAA (Arrange-Act-Assert) pattern"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        # Arrange - test client and activities are already set up
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
        assert "Basketball Team" in activities
        assert "Tennis Club" in activities
        assert "Art Club" in activities
        assert "Drama Club" in activities
        assert "Debate Team" in activities
        assert "Science Club" in activities
    
    def test_get_activities_returns_activity_structure(self, client, reset_activities):
        # Arrange - expected keys for each activity
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == expected_keys


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_for_activity_success(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()["Chess Club"]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
        updated_activities = client.get("/activities").json()
        assert email in updated_activities["Chess Club"]["participants"]
        assert len(updated_activities["Chess Club"]["participants"]) == initial_count + 1
    
    def test_signup_for_nonexistent_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_duplicate_registration_fails(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Art Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act - sign up first student
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        # Sign up second student
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        updated_activities = client.get("/activities").json()
        assert email1 in updated_activities["Art Club"]["participants"]
        assert email2 in updated_activities["Art Club"]["participants"]


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_from_activity_success(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()["Chess Club"]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]
        updated_activities = client.get("/activities").json()
        assert email not in updated_activities["Chess Club"]["participants"]
        assert len(updated_activities["Chess Club"]["participants"]) == initial_count - 1
    
    def test_unregister_nonexistent_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_unregistered_student(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_multiple_students(self, client, reset_activities):
        # Arrange
        activity_name = "Drama Club"
        email1 = "james@mergington.edu"
        email2 = "charlotte@mergington.edu"
        
        # Act - unregister first student
        response1 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email1}
        )
        # Unregister second student
        response2 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        updated_activities = client.get("/activities").json()
        assert email1 not in updated_activities["Drama Club"]["participants"]
        assert email2 not in updated_activities["Drama Club"]["participants"]
        assert len(updated_activities["Drama Club"]["participants"]) == 0


class TestSignupAndUnregisterFlow:
    """Integration tests for complete signup and unregister flow"""
    
    def test_signup_then_unregister_workflow(self, client, reset_activities):
        # Arrange
        activity_name = "Tennis Club"
        email = "integration@mergington.edu"
        
        # Act - sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Verify signup
        activities_after_signup = client.get("/activities").json()
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Verify unregister
        activities_after_unregister = client.get("/activities").json()
        
        # Assert
        assert signup_response.status_code == 200
        assert email in activities_after_signup["Tennis Club"]["participants"]
        assert unregister_response.status_code == 200
        assert email not in activities_after_unregister["Tennis Club"]["participants"]
