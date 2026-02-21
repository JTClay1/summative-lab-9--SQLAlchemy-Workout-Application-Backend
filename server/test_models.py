import pytest
from models import Exercise, Workout, WorkoutExercise
from datetime import date
import sqlalchemy 

def test_exercise_creation_success(db):
    # Verify a valid exercise is successfully saved and assigned an ID
    exercise = Exercise(name="Squat", category="Strength", equipment_needed=True)
    db.session.add(exercise)
    db.session.commit()
    
    assert exercise.id is not None
    assert exercise.name == "Squat"

def test_workout_duration_validation(db):
    # Verify the database CHECK constraint catches invalid durations
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        bad_workout = Workout(date=date.today(), duration_minutes=0, notes="Too short")
        db.session.add(bad_workout)
        db.session.commit()

def test_workout_exercise_reps_validation(db):
    # Verify the model validation catches negative rep counts
    with pytest.raises(ValueError, match="reps cannot be negative"):
        bad_link = WorkoutExercise(workout_id=1, exercise_id=1, reps=-5, sets=3, duration_seconds=0)
        db.session.add(bad_link)
        db.session.commit()