# Flask SQLAlchemy Workout Application Backend

## Project Description
A RESTful API built with Python, Flask, SQLAlchemy, and Marshmallow for managing fitness routines. This backend architecture supports a many-to-many relationship between Workouts and Exercises via a join table (`WorkoutExercise`). It features custom model validations, cascading deletes to prevent orphaned data, and fully serialized JSON responses for seamless frontend integration.

## Installation Instructions

1. Clone the repository to your local machine.

2. Navigate into the project directory:
    cd summative-lab-9--SQLAlchemy-Workout-Application-Backend

3. Install the required dependencies and enter the virtual environment:
    pipenv install
    pipenv shell

4. Navigate to the server directory:
    cd server

5. Setup the database and run the migrations:
    flask db upgrade

6. Seed the database with the initial test data:
    python seed.py


## Run Instructions

-To start the Flask server (runs locally on port `5555`):
    python app.py

-To run the automated test suite (`pytest`):
    python -m pytest


## API Endpoints

-Exercises
    -GET /exercises - Retrieves a list of all exercises.

    -GET /exercises/<id> - Retrieves a specific exercise by its ID.

    -POST /exercises - Creates a new exercise. Requires name, category, and equipment_needed in the JSON body.

    -DELETE /exercises/<id> - Deletes a specific exercise and cascades the deletion to any associated join-table records.

-Workouts
    -GET /workouts - Retrieves a list of all workouts.

    -GET /workouts/<id> - Retrieves a specific workout by its ID. Includes nested exercise data.

    -POST /workouts - Creates a new workout session. Requires date, duration_minutes, and notes in the JSON body.

    -DELETE /workouts/<id> - Deletes a specific workout and cascades the deletion to any associated join-table records.

-Workout Exercises (Join Table)
    -POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Links an existing exercise to an existing workout. Requires reps, sets, and duration_seconds in the JSON body.

