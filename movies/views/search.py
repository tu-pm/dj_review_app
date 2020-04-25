from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .utils import movie_data, paginate
import json



def get_search_results(query):
    res = []
    for index, movie in movie_data.items():
        title = movie['title'].lower()
        if title.find(query.lower()) != -1:
           res.append(index)
    return res


@login_required
def render_template(request):
    query =  request.GET.get('query')
    get_copy = request.GET.copy()
    get_copy.pop('page', True)
    parameters = get_copy.urlencode()

    tmdb_ids = get_search_results(query)
    movies = [movie_data[k] for k in tmdb_ids if k in movie_data]
    movies = paginate(request, movies, 12)
    context = {
        'query': query,
        'movies': movies,
        'parameters': parameters,
    }
    return render(request, 'pages/search.j2', context)
