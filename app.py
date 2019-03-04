import json
from bson.regex import Regex
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'songs'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/songs'

mongo = PyMongo(app)


@app.route('/songs', methods=['GET'])
def get_songs():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 0))

    next_url = "songs?limit={}&offset={}".format(limit, offset+limit)
    prev_url = "songs?limit={}&offset={}".format(limit, max(offset-limit, 0))

    songs = mongo.db.songs.find({}, {'artist': 1, 'title': 1, "_id": 1}).limit(limit).skip(offset)
    output = []
    for s in songs:
        s['_id'] = str(s['_id'])
        output.append(s)
    return jsonify({'result': output, 'next_url': next_url, 'prev_url': prev_url})


@app.route('/songs/avg/difficulty/', methods=['GET'])
def get_average_song_difficulty():
    level = request.args.get('level', None)

    if level:
        result = list(mongo.db.songs.aggregate([
            {
                "$match": {"level": int(level)}
            },
            {"$group": {
                "_id": "null",
                "average": {"$avg": "$difficulty"}
            }
            }
        ]))
    else:
        result = list(mongo.db.songs.aggregate([
            {"$group": {
                "_id": "null",
                "average": {"$avg": "$difficulty"}
            }
            }
        ]))

    return jsonify({'result': result[0]['average'] if result else 'Level not found!'})


@app.route('/songs/search', methods=['GET'])
def search_songs():
    args = request.args['message']
    query = {"$or": [
        {
            u"title": Regex(u"^.*{}.*$".format(args), "i")
        },
        {
            u"artist": Regex(u"^.*{}.*$".format(args), "i")
        }
    ]}

    songs = mongo.db.songs.find(query)
    output = []
    if songs.count():
        for s in songs:
            output.append({'artist': s['artist'], 'title': s['title']})
        return jsonify({'result': output})
    else:
        return jsonify({'result': "No Match!"})


@app.route('/songs/rating', methods=['POST'])
def rate_song():
    allowed_rate_values = [1, 2, 3, 4, 5]
    song_id = json.loads(request.data)['song_id']
    rating = json.loads(request.data)['rating']

    if not int(rating) in allowed_rate_values:
        return jsonify({'result': "Rating should be in range 1,5"}), 400

    try:
        # Find the song
        mongo.db.songs.find_one({'_id': ObjectId(song_id)})

        # add rating to the song in 'song_ratings' collection
        mongo.db.song_rating.insert({'song_id': ObjectId(song_id), 'rating': rating})
        return jsonify({'result': "Rating added!"}), 201
    except:
        return jsonify({'error': "Song id not found!"}), 404


@app.route('/songs/avg/rating/<song_id>', methods=['GET'])
def get_song_rating(song_id):
    try:

        mongo.db.songs.find_one({'_id': ObjectId(song_id)})
    except:
        return jsonify({'result': "No Result!"}), 404

    # Find min max and average value for given song_id
    result = list(mongo.db.song_rating.aggregate([
        {
            "$match": {"song_id": ObjectId(song_id)}
        },
        {"$group": {
            "_id": "null",
            "max_rating": {"$max": "$rating"},
            "min_rating": {"$min": "$rating"},
            "average_rating": {"$avg": "$rating"}
        }
        }
    ]))
    if result:
        return jsonify(
            {'result': {'min': result[0]['min_rating'], 'max': result[0]['max_rating'],
                        'average': result[0]['average_rating']}}), 200
    else:
        return jsonify({'result': "This song is not rated yet!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
