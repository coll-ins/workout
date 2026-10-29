import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))

from app import create_app  # noqa: E402
from models import db  # noqa: E402


@pytest.fixture
def client():
    app = create_app("sqlite:///:memory:")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
