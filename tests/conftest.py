import py
import pytest
from app import create_app
from app.models.word import Word
from app import db

@pytest.fixture
def app():
    # create the app with a teset config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


# fixture that creates three ث ب ت entries and saves them in the database
def add_tha_ba_ta(app):
    db.session.add_all([
        Word(voweled_word= "ثَبَتَ", unvoweled_word="ثبت"),
        Word(voweled_word= "ثُبوت", unvoweled_word="ثبوت"),
        Word(voweled_word= "ثابِت", unvoweled_word="ثابت"),
    ])
    db.session.commit()