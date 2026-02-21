from flask import Flask, make_response, request
from flask_migrate import Migrate
from datetime import datetime 
from models import *
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Instantiate serialization schemas
exercises_schema = ExerciseSchema(many=True)
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()


# Route to get all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    # Serialize the SQLAlchemy objects to JSON
    return exercises_schema.dump(exercises), 200

# Route to get a specific exercise by ID
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    
    # Return 404 if exercise doesn't exist
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404) 
        
    return exercise_schema.dump(exercise), 200

# Route to create a new exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    
    try:
        # Instantiate a new Exercise object from the request data
        new_exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed')
        )
        
        # Stage and commit to the database
        db.session.add(new_exercise)
        db.session.commit()
        
        return exercise_schema.dump(new_exercise), 201
        
    except ValueError as e:
        # Catch model validations and return as a 400 Bad Request
        return make_response({"errors": [str(e)]}, 400) 

# Route to delete an exercise
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()
    
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
        
    # Delete associated join table records first to prevent orphaned data
    WorkoutExercise.query.filter(WorkoutExercise.exercise_id == id).delete() 
    
    db.session.delete(exercise)
    db.session.commit()
    
    # Return empty object and 204 No Content on successful deletion
    return make_response({}, 204)

# Route to get all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200

# Route to get a specific workout by ID
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()
    
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
        
    return workout_schema.dump(workout), 200

# Route to create a new workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    
    try:
        # Convert string to Python date object before saving
        date_str = data.get('date')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None 

        new_workout = Workout(
            date=date_obj,
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        
        db.session.add(new_workout)
        db.session.commit()
        
        return workout_schema.dump(new_workout), 201
        
    except ValueError as e:
        return make_response({"errors": [str(e)]}, 400)
    except Exception as e:
        # Fallback for bad date formats
        return make_response({"errors": ["Invalid data or date format. Use YYYY-MM-DD."]}, 400) 

# Route to delete a workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()
    
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
        
    # Delete associated join table records first to prevent orphaned data
    WorkoutExercise.query.filter(WorkoutExercise.workout_id == id).delete() 
        
    db.session.delete(workout)
    db.session.commit()
    
    return make_response({}, 204)

# Route to add an exercise to a workout (Join Table)
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    # Retrieve parent records
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    
    # Ensure both parent records exist before attempting to link them
    if not workout or not exercise:
        return make_response({"error": "Workout or Exercise not found"}, 404) 

    data = request.get_json()
    
    try:
        # Create the mapping record in the join table
        new_workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        
        db.session.add(new_workout_exercise)
        db.session.commit()
        
        return workout_exercise_schema.dump(new_workout_exercise), 201
        
    except ValueError as e:
        return make_response({"errors": [str(e)]}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)