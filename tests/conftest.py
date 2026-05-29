"""Pytest configuration and fixtures for testing"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture to provide test client"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture to reset activities state before each test"""
    original_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for interscholastic games",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in matches",
            "schedule": "Wednesdays and Saturdays, 10:00 AM - 11:30 AM",
            "max_participants": 16,
            "participants": ["lucas@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Wednesdays and Fridays, 4:30 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["james@mergington.edu", "charlotte@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in debate competitions and develop public speaking skills",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 5:45 PM",
            "max_participants": 18,
            "participants": ["ryan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore STEM concepts",
            "schedule": "Mondays, 3:45 PM - 5:00 PM",
            "max_participants": 24,
            "participants": ["sarah@mergington.edu", "david@mergington.edu"]
        }
    }
    activities.clear()
    activities.update(original_state)
    yield
    activities.clear()
    activities.update(original_state)
