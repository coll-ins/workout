from marshmallow import Schema, ValidationError, fields, validate, validates, validates_schema

from models import EXERCISE_CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(sorted(EXERCISE_CATEGORIES)))
    equipment_needed = fields.Bool(load_default=False)

    @validates("name")
    def validate_name_not_blank(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Name cannot be blank.")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    sets = fields.Int(validate=validate.Range(min=1, max=100), allow_none=True)
    reps = fields.Int(validate=validate.Range(min=1, max=1000), allow_none=True)
    duration_seconds = fields.Int(validate=validate.Range(min=1, max=86400), allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def require_reps_or_duration(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError("Provide reps or duration_seconds.", field_name="reps")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(load_default=None)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(validate=validate.Length(max=500), allow_none=True)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
