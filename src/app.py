"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
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
    "Soccer Team": {
        "description": "Competitive soccer practices and matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": [
            "sam@mergington.edu",
            "lena@mergington.edu",
            "omar@mergington.edu"
        ]
    },
    "Basketball Club": {
        "description": "Skill development and intramural basketball games",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 15,
        "participants": [
            "nina@mergington.edu",
            "liam@mergington.edu",
            "rosa@mergington.edu"
        ]
    },
    "Art Workshop": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": [
            "ava@mergington.edu",
            "noah@mergington.edu",
            "mia@mergington.edu"
        ]
    },
    "Drama Club": {
        "description": "Acting, stagecraft, and school productions",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": [
            "lucas@mergington.edu",
            "zoe@mergington.edu",
            "ethan@mergington.edu"
        ]
    },
    "Debate Team": {
        "description": "Competitive speech and debate practice",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": [
            "grace@mergington.edu",
            "henry@mergington.edu",
            "isabella@mergington.edu"
        ]
    },
    "Science Club": {
        "description": "Hands-on experiments, projects, and science fairs",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": [
            "jack@mergington.edu",
            "sara@mergington.edu",
            "oliver@mergington.edu"
        ]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity.get("participants", []):
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    
    


    # Normalize email and check for duplicates
    email_norm = email.strip().lower()
    participants = activity.get("participants", [])

    if any(p.strip().lower() == email_norm for p in participants):
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Enforce max participants if configured
    max_participants = activity.get("max_participants")
    if isinstance(max_participants, int) and len(participants) >= max_participants:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add normalized email to participants
    participants.append(email_norm)
    activity["participants"] = participants
    return {"message": f"Signed up {email_norm} for {activity_name}"}
