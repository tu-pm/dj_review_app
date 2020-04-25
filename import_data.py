import django
django.setup()


import json
from movies.models import Movie, Genre

movie_data = json.load(open('/home/tupham/web-mining/web_server/dj_review_app/project/movies(2).json', 'r'))


# for tmdb_id, movie in movie_data.items():
#     m = Movie(
#         tmdb_id=tmdb_id,
#         title=movie['title'],
#         overview=movie['overview'],
#         release_date=movie['release_date'],
#         poster_path=movie['poster_path'],
#         backdrop_path=movie['backdrop_path'],
#     )
#     print(m)
#     m.save()


for tmdb_id, movie in movie_data.items():
    m = Movie.objects.filter(tmdb_id=tmdb_id)[0]
    for genre in movie['genres']:
        g = Genre(name=genre['name'], movie=m)
        g.save()
