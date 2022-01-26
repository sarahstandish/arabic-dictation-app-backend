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

# fixture that adds one word
@pytest.fixture
def add_one_word(app):
    db.session.add(Word(voweled_word= "ثُبوت", unvoweled_word="ثبوت"))
    db.session.commit()

# fixture that creates three ث ب ت entries and saves them in the database
@pytest.fixture
def add_three_words(app):
    db.session.add_all([
        Word(voweled_word= "ثَبَتَ", unvoweled_word="ثبت"),
        Word(voweled_word= "ثُبوت", unvoweled_word="ثبوت"),
        Word(voweled_word= "ثابِت", unvoweled_word="ثابت"),
    ])
    db.session.commit()

@pytest.fixture
def add_eleven_words(app):
    db.session.add_all([
        Word(voweled_word= "ثَبَتَ", unvoweled_word="ثبت"),
        Word(voweled_word= "ثُبوت", unvoweled_word="ثبوت"),
        Word(voweled_word= "ثابِت", unvoweled_word="ثابت"),
        Word(voweled_word= "عَلَى", unvoweled_word="على"),
        Word(voweled_word= "أَنْ", unvoweled_word="أن"),
        Word(voweled_word= "آخَر", unvoweled_word="آخر"),
        Word(voweled_word= "شَيْء", unvoweled_word="شيء"),
        Word(voweled_word= "مُؤَسَّسَة", unvoweled_word="مؤسسة"),
        Word(voweled_word= "اِسْتَخْدَمَ", unvoweled_word="استخدم"),
        Word(voweled_word= "مُتَوَسِّط", unvoweled_word="متوسط"),
        Word(voweled_word= "إِلِكْترُونِيّ", unvoweled_word="إلكتروني"),
    ])
    db.session.commit()