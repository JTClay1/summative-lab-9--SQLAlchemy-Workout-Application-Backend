from marshmallow import Schema, fields, validate

# Schema for Exercise 
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True) 
    name = fields.Str(required=True, validate=validate.Length(min=3, error="Name must be at least 3 characters"))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()
    
    # Nested relationship to show where this exercise is used
    workout_exercises = fields.Nested("WorkoutExerciseSchema", many=True, exclude=("exercise_id",))

# Schema for Workout
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True) 
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Duration cannot be less than 1 minute"))
    notes = fields.Str()
    
    # Nested relationship to show all exercises in this workout
    workout_exercises = fields.Nested("WorkoutExerciseSchema", many=True, exclude=("workout_id",))
    
# Schema for WorkoutExercise (The Join Table)
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True) 
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    
    # Updated validations to min=0 to allow purely rep-based or time-based exercises
    reps = fields.Int(required=True, validate=validate.Range(min=0, error="Reps cannot be less than 0"))
    sets = fields.Int(required=True, validate=validate.Range(min=0, error="Sets cannot be less than 0"))
    duration_seconds = fields.Int(required=True, validate=validate.Range(min=0, error="Duration cannot be less than 0 seconds"))
    
    # Nested relationship to show the actual exercise details (like name and category)
    exercise = fields.Nested("ExerciseSchema", exclude=("workout_exercises",))