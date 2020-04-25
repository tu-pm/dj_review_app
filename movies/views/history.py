from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .utils import movie_data, paginate
from ..models import Rating


def get_reviewed_movies(user):
    movies = []
    ratings = Rating.objects.filter(user=user)
    for rating in ratings:
        movie = movie_data[rating.movie]
        movie['user_rating'] = int(rating.score)
        movies.append(movie)
    return movies


@login_required
def render_template(request):
    movies = get_reviewed_movies(request.user)
    movies = paginate(request, movies, 5)
    context = {
        'movies': movies
    }
    return render(request, 'pages/history.j2', context)
