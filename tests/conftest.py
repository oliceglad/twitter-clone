import sys

import pytest

from app.database import Base, engine, session
from app.models import Followers, Like, Tweet, User
from app.routes import create_app

sys.path.append("..")


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True

    with _app.app_context():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        objects = [
            User(name="test", email="test@test.ru", token="test"),
            User(name="test1", email="test1@test.ru", token="test1"),
            Tweet(text="text", author_id=2),
            Followers(user_id=2, follower_id=1),
            Like(user_id=1, tweet_id=1),
        ]
        session.bulk_save_objects(objects)
        session.commit()

        yield _app

        session.close()

        Base.metadata.drop_all(engine)


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield session
