from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.conf import settings
import requests, json
from django.contrib.auth.forms import UserCreationForm
import requests, json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Rating


HOSTNAME = '10.71.0.169'
HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

movie_data = json.load(open('/home/tupham/web-mining/server/dj_review_app/project/movies.json', 'r'))

def get_related_tmdb_ids(tmdb_id):
    url='http://{}:8000/sim?movie_id={}'.format(HOSTNAME, tmdb_id)
    res = requests.get(
                url= url,
                headers= HEADERS,
            )
    return json.loads(res.content)['movies']


def get_recommended_tmdb_ids(user_id):
    url='http://{}:8000/recommend?user_id={}'.format(HOSTNAME, user_id)
    res = requests.get(
                url=url,
                headers=HEADERS,
            )
    x = json.loads(res.content)['movies']
    print(x)
    return x

##############
# GET methods:
##############

def get_search_results(query):
    res = []
    for index, movie in movie_data.items():
        title = movie['title'].lower()
        if title.find(query.lower()) != -1:
           res.append(index)
    return res


def get_related_movies(tmdb_id):
    return list(movie_data.keys())[0:20]


def get_recommended_movies(user_id):
    return list(movie_data.keys())[20:40]


def get_trending_movies():
    return list(movie_data.keys())[40:60]


###############
# POST methods:
###############

@method_decorator(csrf_exempt, name='dispatch')
def send_rating(request):
    user_id = request.user.id
    rating = request.POST.get('rating')
    movie_id = request.POST.get('movie_id')
    r = Rating(user=request.user, movie=movie_id, score=rating)
    r.save()
    print(user_id, rating, movie_id)
    url='http://{}:8000/add_rating'.format(HOSTNAME)
    data = {'user_id': user_id, 'movie_id': movie_id, 'rating': rating}
    res = requests.post(url=url, data=data)
    return JsonResponse({})


def add_new_user(user_id):
    url='http://{}:8000/add_user?user_id={}'.format(HOSTNAME, user_id)
    requests.get(url=url)


def paginate(request, items, items_per_page):
    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return items


###############
# VIEW methods:
###############

@login_required
def home(request):
    tmdb_ids = get_recommended_movies(request.user.id)
    movies = [movie_data[k] for k in tmdb_ids if k in movie_data]
    context = {
        'movies': movies,
    }
    return render(request, 'pages/home.j2', context)

@login_required
def search(request):
    query =  request.GET.get('query')
    tmdb_ids = get_tmdb_ids(query)
    movies = [movie_data[k] for k in tmdb_ids if k in movie_data]
    movies = paginate(request, movies, 4)
    context = {
        'query': query,
        'movies': movies,
    }
    return render(request, 'pages/search.j2', context)


@login_required
def details(request, num=0):
    tmdb_ids = get_related_tmdb_ids(str(num))
    related = [movie_data[k] for k in tmdb_ids if k in movie_data]
    try:
        rated = Rating.objects.filter(movie=num, user=request.user)[0].score
    except:
        rated = 0

    context = {
            'rated': rated,
            'current': movie_data.get(str(num)),
            'related': paginate(request, related, 4)
    }
    return render(request, 'pages/details.j2', context)


@login_required
def history(request):
    context = {}
    return render(request, 'pages/history.j2', context)



@login_required
def trending(request):
    context = {}
    return render(request, 'pages/trending.j2', context)


