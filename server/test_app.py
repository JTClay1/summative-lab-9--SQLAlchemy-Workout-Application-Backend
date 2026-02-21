import pytest
from app import app, db
from models import Exercise, Workout

def test_get_exercises_status_code(client):
    # Verify the GET route returns a successful 200 response
    response = client.get('/exercises')
    assert response.status_code == 200

def test_create_workout_success(client):
    # Verify the POST route creates a record and returns a 201 Created response
    response = client.post('/workouts', json={
        "date": "2026-03-01",
        "duration_minutes": 60,
        "notes": "Testing the suite!"
    })
    assert response.status_code == 201

def test_exercise_validation_fails_properly(client):
    # Verify the POST route catches invalid data and returns a 400 Bad Request
    response = client.post('/exercises', json={
        "name": "A", 
        "category": "Strength",
        "equipment_needed": False
    })
    
    assert response.status_code == 400
    assert "Exercise name must be at least 3 characters long." in response.get_data(as_text=True)