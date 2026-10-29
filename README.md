# Workout Tracker API

Flask + SQLAlchemy + Marshmallow backend for a workout tracking app used by personal trainers.
Workouts contain reusable exercises; each link stores sets, reps and/or duration.

## Models
- **Exercise**: `name` (unique), `category`, `equipment_needed`
- **Workout**: `date`, `duration_minutes`, `notes`
- **WorkoutExercise** (join): `workout_id`, `exercise_id`, `sets`, `reps`, `duration_seconds`

Relationships: Workout many-to-many Exercise through WorkoutExercise. Deleting a workout or exercise deletes its join rows.

## Validations
- **Table constraints**: unique exercise name, non-blank name, `duration_minutes > 0`, unique (workout, exercise) pair, positive sets/reps/duration, reps or duration required.
- **Model validations** (`@validates`): exercise name and category, workout duration and notes length, positive integers on join fields.
- **Schema validations** (Marshmallow): length/range/OneOf validators, `@validates` blank-name check, `@validates_schema` requiring reps or duration.

## Installation
```bash
pipenv install
pipenv shell
export FLASK_APP=app.py
cd server
flask db upgrade
python seed.py
```

## Run
```bash
cd server
flask run -p 5555
```

## Tests
```bash
pipenv install --dev
pipenv run pytest
```

## Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/workouts` | List all workouts (newest first) |
| GET | `/workouts/<id>` | One workout with its exercises, sets, reps, duration |
| POST | `/workouts` | Create workout. Body: `duration_minutes` (required), `date` (YYYY-MM-DD, optional), `notes` |
| DELETE | `/workouts/<id>` | Delete workout |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | One exercise |
| POST | `/exercises` | Create exercise. Body: `name`, `category` (strength, cardio, flexibility, balance), `equipment_needed` |
| DELETE | `/exercises/<id>` | Delete exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add exercise to workout. Body: `sets`, `reps` and/or `duration_seconds` |

Errors: 400 validation, 404 not found, 409 duplicate.
