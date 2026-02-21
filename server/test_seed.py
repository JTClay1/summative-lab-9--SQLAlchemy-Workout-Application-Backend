import pytest
from models import Exercise, Workout
from seed import seed_data 

def test_seed_populates_data(db, app):
    # Run the seed function within the application context
    with app.app_context():
        seed_data() 
    
    # Verify that data was successfully added to the database
    assert Exercise.query.count() > 0
    assert Workout.query.count() > 0