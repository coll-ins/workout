from datetime import date, timedelta

from app import app
from models import Exercise, Workout, WorkoutExercise, db

with app.app_context():
    print("Clearing tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    exercises = [
        Exercise(name="Squat", category="strength", equipment_needed=True),
        Exercise(name="Push-up", category="strength", equipment_needed=False),
        Exercise(name="Running", category="cardio", equipment_needed=False),
        Exercise(name="Plank", category="strength", equipment_needed=False),
        Exercise(name="Hamstring Stretch", category="flexibility", equipment_needed=False),
    ]
    db.session.add_all(exercises)

    today = date.today()
    workouts = [
        Workout(date=today, duration_minutes=45, notes="Leg day"),
        Workout(date=today - timedelta(days=2), duration_minutes=30, notes="Cardio + core"),
        Workout(date=today - timedelta(days=4), duration_minutes=60),
    ]
    db.session.add_all(workouts)
    db.session.flush()

    squat, pushup, running, plank, stretch = exercises
    db.session.add_all([
        WorkoutExercise(workout=workouts[0], exercise=squat, sets=4, reps=8),
        WorkoutExercise(workout=workouts[0], exercise=stretch, duration_seconds=120),
        WorkoutExercise(workout=workouts[1], exercise=running, duration_seconds=1200),
        WorkoutExercise(workout=workouts[1], exercise=plank, sets=3, duration_seconds=60),
        WorkoutExercise(workout=workouts[2], exercise=pushup, sets=3, reps=15),
        WorkoutExercise(workout=workouts[2], exercise=squat, sets=5, reps=5),
    ])
    db.session.commit()
    print("Seeded exercises, workouts, and workout_exercises.")
