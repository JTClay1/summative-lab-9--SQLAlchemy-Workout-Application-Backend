from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    # Table Constraints: name must be unique and cannot be empty (nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    # Model Validation 1: Ensure name is at least 3 characters
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError("Exercise name must be at least 3 characters long.")
        return name

    # Model Validation 2: Restrict category to specific acceptable strings
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Strength', 'Cardio', 'Flexibility', 'Mobility']
        if category and category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

    def __repr__(self):
        return f'<Exercise {self.name}>'

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date) 
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.String) 

    # Table Constraint: duration must be greater than 0
    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Workout {self.id} on {self.date}>'

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Table Constraints: reps and sets cannot be negative
    __table_args__ = (
        db.CheckConstraint('reps >= 0', name='check_reps_non_negative'),
        db.CheckConstraint('sets >= 0', name='check_sets_non_negative'),
    )

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Model Validation 3: Ensure reps and sets are not negative at the Python level
    @validates('reps', 'sets')
    def validate_positive_integers(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative.")
        return value

    def __repr__(self):
        return f'<WorkoutExercise Workout:{self.workout_id} Exercise:{self.exercise_id}>'