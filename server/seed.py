#!/usr/bin/env python3

from datetime import date
from app import app
from models import *

with app.app_context():
    # Clear All Table data
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    # Create Exercises
    exercise1 = Exercise(name="Pushups", category="Strength", equipment_needed=False)
    exercise2 = Exercise(name="Wind Sprints", category="Cardio", equipment_needed=False)
    exercise3 = Exercise(name="Dumbbell Curls", category="Strength", equipment_needed=True)
    # Stage them, then save them
    db.session.add_all([exercise1, exercise2, exercise3])
    db.session.commit()

    #Create Workouts
    workout1 = Workout(date=date(2026, 2, 24), duration_minutes=20, notes="Upper Body")
    workout2 = Workout(date=date(2026, 2, 26), duration_minutes=20, notes="Cardio")
    workout3 = Workout(date=date(2026, 2, 28), duration_minutes=30, notes="Cardio + Pushups")
    # Stage them, then save them
    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()
    # Create the Links (WorkoutExercises)
    # Linking workout1 (Upper Body) to exercise1 (Pushups)
    link1 = WorkoutExercise(workout=workout1, exercise=exercise1, reps=15, sets=3, duration_seconds=600)
    # Linking workout1 (Upper Body) to exercise3 (Dumbbell Curls)
    link2 = WorkoutExercise(workout=workout1, exercise=exercise3, reps=12, sets=3, duration_seconds=600)
    # Linking workout2 (Cardio) to exercise2 (Wind Sprints)
    link3 = WorkoutExercise(workout=workout2, exercise=exercise2, reps=3, sets=5, duration_seconds=1200)
    # Linking workout3 (Cardio + Pushups) to exercise2 (Wind Sprints)
    link4 = WorkoutExercise(workout=workout3, exercise=exercise2, reps=3, sets=5, duration_seconds=1200)
    # Linking workout3 (Cardio + Pushups) to exercise1 (Pushups)
    link5 = WorkoutExercise(workout=workout3, exercise=exercise1, reps=15, sets=3, duration_seconds=600)

    # Stage them, then save them
#!/usr/bin/env python3

from app import app
from models import *

with app.app_context():
    # Clear All Table data
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    # Create Exercises
    exercise1 = Exercise(name="Pushups", category="Strength", equipment_needed=False)
    exercise2 = Exercise(name="Wind Sprints", category="Cardio", equipment_needed=False)
    exercise3 = Exercise(name="Dumbbell Curls", category="Strength", equipment_needed=True)
    # Stage them, then save them
    db.session.add_all([exercise1, exercise2, exercise3])
    db.session.commit()

    #Create Workouts
    workout1 = Workout(date=date(2026, 2, 24), duration_minutes=20, notes="Upper Body")
    workout2 = Workout(date=date(2026, 2, 26), duration_minutes=20, notes="Cardio")
    workout3 = Workout(date=date(2026, 2, 28), duration_minutes=30, notes="Cardio + Pushups")
    # Stage them, then save them
    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()
    # Create the Links (WorkoutExercises)
    # Linking workout1 (Upper Body) to exercise1 (Pushups)
    link1 = WorkoutExercise(workout=workout1, exercise=exercise1, reps=15, sets=3, duration_seconds=600)
    # Linking workout1 (Upper Body) to exercise3 (Dumbbell Curls)
    link2 = WorkoutExercise(workout=workout1, exercise=exercise3, reps=12, sets=3, duration_seconds=600)
    # Linking workout2 (Cardio) to exercise2 (Wind Sprints)
    link3 = WorkoutExercise(workout=workout2, exercise=exercise2, reps=3, sets=5, duration_seconds=1200)
    # Linking workout3 (Cardio + Pushups) to exercise2 (Wind Sprints)
    link4 = WorkoutExercise(workout=workout3, exercise=exercise2, reps=3, sets=5, duration_seconds=1200)
    # Linking workout3 (Cardio + Pushups) to exercise1 (Pushups)
    link5 = WorkoutExercise(workout=workout3, exercise=exercise1, reps=15, sets=3, duration_seconds=600)

    # Stage them, then save them
    db.session.add_all([link1, link2, link3, link4, link5]) 
    db.session.commit()