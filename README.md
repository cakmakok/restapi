restapi uses flask and mongodb. 

Installation:
To run the app, you need docker in your system.
Dockers brings up the web server-mongodb and also seeds mongodb with initial songs database.
All you need to do is to run:

- docker-compose build
- docker-compose up


Usage:
- GET /songs
  - Returns a list of song title, artist and song_id
  - Takes optional parameters for pagination:
      -limit : number of results per page.
      -offset : start index of the first song in the result page
      pagination usage example link : /songs?limit=10&offset=0 for 10 results per page
      
- GET /songs/avg/difficulty
  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.
  example link with optional level parameter /songs/avg/difficulty?level=13 : for average dificulty of the songs in 13. level

- GET /songs/search
  - Takes in parameter a 'message' string to search.
  - Return a list of songs that includes search parameter.
  example link /songs/search?message=opa : searches keyword "opa" in the song title or artist info

- POST /songs/rating
  - Takes in parameter a "song_id" and a "rating"
  - This call adds a rating to the song. Ratings should be between 1 and 5.
  example payload:
      {
          "song_id":"",
          "rating": 4
      }

- GET /songs/avg/rating/<song_id>
  - Returns the average, the lowest and the highest rating of the given song id.
