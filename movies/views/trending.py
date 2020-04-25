from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .utils import movie_data, paginate, get_rating
import heapq

sorted_movies = [get_rating(movie) for movie in movie_data.values()]
sorted_movies = heapq.nlargest(10, sorted_movies, key=lambda x: x['vote_count'])

def get_trending_movies():
    movies = sorted(sorted_movies, key=lambda x: -x['vote_count'])
    return movies

@login_required
def render_template(request):
    movies = get_trending_movies()
    movies = paginate(request, movies, 5)
    context = {
        'movies': movies
    }
    return render(request, 'pages/trending.j2', context)

