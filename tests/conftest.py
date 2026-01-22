import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store initial state
    initial_activities = {
        "Chess Club": {
            "Basketball Team": {
                "description": "Join the school basketball team and compete in local leagues",
                "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
                "max_participants": 15,
                "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
            },
            "Soccer Club": {
                "description": "Practice soccer skills and play friendly matches",
                "schedule": "Saturdays, 10:00 AM - 12:00 PM",
                "max_participants": 20,
                "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
            },
            "Art Workshop": {
                "description": "Explore painting, drawing, and sculpture techniques",
                "schedule": "Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 10,
                "participants": ["ava@mergington.edu", "liam@mergington.edu"]
            },
            "Drama Club": {
                "description": "Act, direct, and produce school plays and performances",
                "schedule": "Mondays, 4:00 PM - 5:30 PM",
                "max_participants": 18,
                "participants": ["ella@mergington.edu", "noah@mergington.edu"]
            },
            "Math Olympiad": {
                "description": "Prepare for math competitions and solve challenging problems",
                "schedule": "Tuesdays, 5:00 PM - 6:00 PM",
                "max_participants": 12,
                "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
            },
            "Science Club": {
                "description": "Conduct experiments and explore scientific concepts",
                "schedule": "Fridays, 2:30 PM - 4:00 PM",
                "max_participants": 16,
                "participants": ["charlotte@mergington.edu", "benjamin@mergington.edu"]
            },
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
        }
    }
    
    yield
    
    # Restore initial state
    activities.clear()
    activities.update(initial_activities)
