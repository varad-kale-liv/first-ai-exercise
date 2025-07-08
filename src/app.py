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
    # Sports Activities
    "Basketball Team": {
        "description": "Competitive basketball team with practices and games against other schools",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Learn swimming techniques and participate in swim meets",
        "schedule": "Tuesdays and Thursdays, 6:00 AM - 7:30 AM",
        "max_participants": 25,
        "participants": ["maya@mergington.edu"]
    },
    # Artistic Activities
    "Drama Club": {
        "description": "Act in school plays, learn theater skills, and explore creative expression",
        "schedule": "Mondays and Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["luna@mergington.edu", "jacob@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Create paintings, sculptures, and digital art in a collaborative studio environment",
        "schedule": "Wednesdays, 3:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["zoe@mergington.edu", "ethan@mergington.edu"]
    },
    # Intellectual Activities
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills through competitive debates",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "noah@mergington.edu", "grace@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science and engineering challenges at regional and state levels",
        "schedule": "Saturdays, 9:00 AM - 12:00 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "sophia@mergington.edu"]
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
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail=f"Student {email} is already signed up for {activity_name}")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
