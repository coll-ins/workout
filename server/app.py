import os
from datetime import date

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Exercise, Workout, WorkoutExercise, db
from schemas import (
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(db_uri=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri or "sqlite:///" + os.path.join(
        BASE_DIR, "app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.compact = False

    db.init_app(app)
    Migrate(app, db)
    register_routes(app)
    return app


def register_routes(app):
    @app.errorhandler(ValidationError)
    def handle_schema_error(err):
        return jsonify({"errors": err.messages}), 400

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"error": "Not found"}), 404

    @app.get("/workouts")
    def list_workouts():
        return jsonify(workouts_schema.dump(Workout.query.order_by(Workout.date.desc()).all())), 200

    @app.get("/workouts/<int:id>")
    def get_workout(id):
        return jsonify(workout_schema.dump(db.get_or_404(Workout, id))), 200

    @app.post("/workouts")
    def create_workout():
        data = workout_schema.load(request.get_json(silent=True) or {})
        try:
            workout = Workout(
                date=data.get("date") or date.today(),
                duration_minutes=data["duration_minutes"],
                notes=data.get("notes"),
            )
        except ValueError as e:
            return jsonify({"errors": str(e)}), 400
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201

    @app.delete("/workouts/<int:id>")
    def delete_workout(id):
        db.session.delete(db.get_or_404(Workout, id))
        db.session.commit()
        return "", 204

    @app.get("/exercises")
    def list_exercises():
        return jsonify(exercises_schema.dump(Exercise.query.order_by(Exercise.name).all())), 200

    @app.get("/exercises/<int:id>")
    def get_exercise(id):
        return jsonify(exercise_schema.dump(db.get_or_404(Exercise, id))), 200

    @app.post("/exercises")
    def create_exercise():
        data = exercise_schema.load(request.get_json(silent=True) or {})
        try:
            exercise = Exercise(**data)
        except ValueError as e:
            return jsonify({"errors": str(e)}), 400
        db.session.add(exercise)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"errors": "An exercise with that name already exists."}), 409
        return jsonify(exercise_schema.dump(exercise)), 201

    @app.delete("/exercises/<int:id>")
    def delete_exercise(id):
        db.session.delete(db.get_or_404(Exercise, id))
        db.session.commit()
        return "", 204

    @app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
    def add_exercise_to_workout(workout_id, exercise_id):
        workout = db.get_or_404(Workout, workout_id)
        exercise = db.get_or_404(Exercise, exercise_id)
        data = workout_exercise_schema.load(request.get_json(silent=True) or {})
        try:
            link = WorkoutExercise(workout=workout, exercise=exercise, **data)
        except ValueError as e:
            return jsonify({"errors": str(e)}), 400
        db.session.add(link)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"errors": "Exercise already added to this workout."}), 409
        return jsonify(workout_exercise_schema.dump(link)), 201


app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
