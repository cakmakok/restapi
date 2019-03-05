
import unittest
from app import app
from flask_pymongo import PyMongo
import json


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.mongo = PyMongo(app)


    def test_get_song_list(self):
        result = json.loads(self.app.get('/songs').data)
        songs = self.mongo.db.songs.find({}, {'artist': 1, 'title': 1, "_id": 1})
        output = []
        for s in songs:
            s['_id'] = str(s['_id'])
            output.append(s)
        assert result['result'] == output

    def test_get_average_difficulty(self):
        result = json.loads(self.app.get('/songs/avg/difficulty/').data)
        assert result['result'] == float('10.323636363636364')


if __name__ == '__main__':
    unittest.main()
