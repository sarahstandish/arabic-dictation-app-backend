# Arabic Dictation App
Arabic Dictation App is a tool for Arabic learners to practice the Arabic alphabet. View the live web app [here](https://arabic-dictation-app.herokuapp.com/).  The back end is hosted [here](https://arabic-dictation-api.herokuapp.com/)

## Author
This app was created by [Sarah Standish](https://github.com/sarahstandish/)

## Major features - back end
- The database contains more than 5000 Arabic words drawn from [A Frequency Dictionary of Arabic: Core Vocabulary for Learners](https://www.goodreads.com/book/show/4805313-a-frequency-dictionary-of-arabic).
- Audio files for each word were recorded using the Zeina voice of [AWS Polly](https://aws.amazon.com/polly/).
- The route `GET /words` with no query parameters returns 10 words randomly selected from the database
- The same route with a `GET /words?letters=` query parameter returns up to ten words containing _only_ the letters passed in the query string

## Minor features
- Eight tests (four tests of the route with and without query parameters and four tests of error messages) confirm that major features are functioning.
- Auxiliary text processing module can be used to clean text in a csv, remove vowels, create audio files using a text-to-speech api, and upload resulting files to Google Cloud Storage
- Each word file is named via a hex digest of the MD5 hash of the voweled version of the word, so that filenames can always be re-generated, files can be found by knowing the voweled word, and audio files can be replaced periodically if an improved text-to-speech API is available

## Motivation for this project
This project was motivated by my years of teaching Arabic.  Learning Arabic the Arabic alphabet is a major barrier for students; when I was teaching, I noticed that the majority of students who dropped out of Arabic did so within the first six months of study and that students who had not mastered the alphabet were the most likely to drop out.  Meanwhile, students who were able to master the sound-shape pairings of the Arabic alphabet within this time frame were likely to continue their study at least for another year.  Dictation was an activity I frequently did in class with students, and it was extremely helpful in terms of their ability to recognize Arabic letter sounds and accurately pair these sounds with the relevant shapes.  However, it took me a long time to give crucial individual feedback to each student.  I wished for an app that would give quick and accurate feedback to students.

I completed this project as my final capstone project during my time at [Ada Developer's Academy](https://adadevelopersacademy.org/) in February 2022.

## Tech stack
- Database: [PostgreSQL](https://www.postgresql.org/)
- [Backend](https://github.com/sarahstandish/arabic-dictation-app-backend): [Python](https://www.python.org/), [Flask](https://palletsprojects.com/p/flask/)
- [Frontend](https://github.com/sarahstandish/arabic-dictation-app-front-end): [React](https://reactjs.org/), [JavaScript](https://www.javascript.com/), [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML), [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
- Fonts: [Google Fonts](https://fonts.google.com/)
- Web hosting: [Heroku](https://www.heroku.com/)
- Text-to-speech: [AWS Polly](https://aws.amazon.com/polly/)
- Audio file hosting: [Google Cloud Storage](https://cloud.google.com/storage)

## License
[CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.en_GB)