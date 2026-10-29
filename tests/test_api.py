def make_exercise(client, name="Squat", category="strength"):
    return client.post("/exercises", json={"name": name, "category": category})


def make_workout(client, minutes=30):
    return client.post("/workouts", json={"duration_minutes": minutes, "date": "2026-10-01"})


def test_create_and_get_exercise(client):
    r = make_exercise(client)
    assert r.status_code == 201
    assert client.get(f"/exercises/{r.json['id']}").json["name"] == "Squat"


def test_duplicate_exercise_conflict(client):
    make_exercise(client)
    assert make_exercise(client).status_code == 409


def test_invalid_category_rejected(client):
    assert make_exercise(client, category="magic").status_code == 400


def test_invalid_duration_rejected(client):
    assert client.post("/workouts", json={"duration_minutes": 0}).status_code == 400


def test_add_exercise_to_workout_and_serialize(client):
    e = make_exercise(client).json
    w = make_workout(client).json
    r = client.post(f"/workouts/{w['id']}/exercises/{e['id']}/workout_exercises",
                    json={"sets": 3, "reps": 10})
    assert r.status_code == 201
    body = client.get(f"/workouts/{w['id']}").json
    assert body["workout_exercises"][0]["exercise"]["name"] == "Squat"


def test_requires_reps_or_duration(client):
    e = make_exercise(client).json
    w = make_workout(client).json
    r = client.post(f"/workouts/{w['id']}/exercises/{e['id']}/workout_exercises", json={"sets": 3})
    assert r.status_code == 400


def test_duplicate_link_conflict(client):
    e = make_exercise(client).json
    w = make_workout(client).json
    url = f"/workouts/{w['id']}/exercises/{e['id']}/workout_exercises"
    client.post(url, json={"reps": 5})
    assert client.post(url, json={"reps": 5}).status_code == 409


def test_delete_workout_cascades(client):
    e = make_exercise(client).json
    w = make_workout(client).json
    client.post(f"/workouts/{w['id']}/exercises/{e['id']}/workout_exercises", json={"reps": 5})
    assert client.delete(f"/workouts/{w['id']}").status_code == 204
    assert client.get(f"/workouts/{w['id']}").status_code == 404
    assert client.get(f"/exercises/{e['id']}").status_code == 200


def test_404s(client):
    assert client.get("/workouts/999").status_code == 404
    assert client.delete("/exercises/999").status_code == 404
