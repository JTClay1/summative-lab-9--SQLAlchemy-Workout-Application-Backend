import pytest
from models import Exercise, Workout, WorkoutExercise
from schemas import WorkoutSchema
from datetime import date

def test_workout_schema_nesting(db):
    # Setup mock objects in the temporary database
    ex = Exercise(name="Deadlift", category="Strength", equipment_needed=True)
    wk = Workout(date=date.today(), duration_minutes=30, notes="Heavy Day")
    db.session.add_all([ex, wk])
    db.session.commit()

    # Create the join table link
    link = WorkoutExercise(workout_id=wk.id, exercise_id=ex.id, reps=5, sets=5, duration_seconds=0)
    db.session.add(link)
    db.session.commit()

    # Serialize the workout data using the schema
    schema = WorkoutSchema()
    result = schema.dump(wk)

    # Verify the schema successfully nested the workout exercises
    assert "workout_exercises" in result
    assert len(result["workout_exercises"]) == 1
    assert result["workout_exercises"][0]["exercise"]["name"] == "Deadlift"