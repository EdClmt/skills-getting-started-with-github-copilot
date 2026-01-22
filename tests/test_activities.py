"""
Tests for the Mergington High School Activities API
"""

import pytest


class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Check that all expected activities are present
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
    
    def test_get_activities_contains_activity_details(self, client, reset_activities):
        """Test that activities contain required fields"""
        response = client.get("/activities")
        data = response.json()
        
        activity = data["Programming Class"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
    
    def test_get_activities_participants_list(self, client, reset_activities):
        """Test that participants list is returned correctly"""
        response = client.get("/activities")
        data = response.json()
        
        participants = data["Programming Class"]["participants"]
        assert isinstance(participants, list)
        assert len(participants) > 0
        assert "emma@mergington.edu" in participants


class TestSignupForActivity:
    def test_signup_for_activity_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
    
    def test_signup_adds_participant(self, client, reset_activities):
        """Test that signup actually adds the participant"""
        client.post(
            "/activities/Programming%20Class/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        response = client.get("/activities")
        participants = response.json()["Programming Class"]["participants"]
        assert "newstudent@mergington.edu" in participants
    
    def test_signup_duplicate_email_fails(self, client, reset_activities):
        """Test that signing up with same email twice fails"""
        # First signup should succeed
        response1 = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]
    
    def test_signup_for_nonexistent_activity_fails(self, client, reset_activities):
        """Test that signup for nonexistent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregisterFromActivity:
    def test_unregister_from_activity_success(self, client, reset_activities):
        """Test successful unregister from an activity"""
        response = client.delete(
            "/activities/Programming%20Class/unregister",
            params={"email": "emma@mergington.edu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister actually removes the participant"""
        client.delete(
            "/activities/Programming%20Class/unregister",
            params={"email": "emma@mergington.edu"}
        )
        
        response = client.get("/activities")
        participants = response.json()["Programming Class"]["participants"]
        assert "emma@mergington.edu" not in participants
    
    def test_unregister_nonexistent_student_fails(self, client, reset_activities):
        """Test that unregistering a student not in the activity fails"""
        response = client.delete(
            "/activities/Programming%20Class/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client, reset_activities):
        """Test that unregister from nonexistent activity returns 404"""
        response = client.delete(
            "/activities/Nonexistent%20Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestActivityConstraints:
    def test_max_participants_not_enforced_on_signup(self, client, reset_activities):
        """Test signup behavior (note: current implementation doesn't enforce max)"""
        # This test documents current behavior where max_participants is stored
        # but not enforced during signup
        response = client.get("/activities")
        activity = response.json()["Programming Class"]
        
        assert "max_participants" in activity
        assert activity["max_participants"] == 20
    
    def test_activity_has_schedule_info(self, client, reset_activities):
        """Test that activities contain schedule information"""
        response = client.get("/activities")
        activity = response.json()["Programming Class"]
        
        assert "schedule" in activity
        assert "3:30 PM" in activity["schedule"]
