from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .utils import movie_data, paginate, get_rating, HOSTNAME, HEADERS
import requests, json


def get_recommended_movies(user_id):
    url='http://{}:8000/recommend?user_id={}'.format(HOSTNAME, user_id)
    res = requests.get(
                url=url,
                headers=HEADERS,
            )
    x = json.loads(res.content)['movies']
    print(x)
    return x

@login_required
def render_template(request):
    tmdb_ids = get_recommended_movies(request.user.id)
    movies = [get_rating(movie_data[k]) for k in tmdb_ids if k in movie_data]
    movies = paginate(request, movies, 12)
    context = {
        'movies': movies,
    }
    return render(request, 'pages/home.j2', context)
