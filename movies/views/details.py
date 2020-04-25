from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import JsonResponse
from .utils import movie_data, paginate, get_rating, HOSTNAME, HEADERS
from ..models import Rating
import requests, json


def get_related_movies(tmdb_id):
    url='http://{}:8000/sim?movie_id={}'.format(HOSTNAME, tmdb_id)
    res = requests.get(
                url= url,
                headers= HEADERS,
            )
    return json.loads(res.content)['movies']

@login_required
def render_template(request, num=0):
    tmdb_ids = get_related_movies(str(num))
    related = [get_rating(movie_data[k]) for k in tmdb_ids if k in movie_data]
    try:
        rated = Rating.objects.filter(movie=num, user=request.user).last().score
    except:
        rated = 0

    context = {
            'rated': rated,
            'current': get_rating(movie_data.get(str(num))),
            'related': paginate(request, related, 4)
    }
    return render(request, 'pages/details.j2', context)



@method_decorator(csrf_exempt, name='dispatch')
def add_rating(request):
    user_id = request.user.id
    rating = request.POST.get('rating')
    movie_id = request.POST.get('movie_id')
    try:
        r = Rating.objects.get(user=request.user, movie=movie_id)
        r.score=rating
        r.save()
    except:
        r = Rating(user=request.user, movie=movie_id, score=rating)
        r.save()
    print(user_id, rating, movie_id)
    url='http://{}:8000/add_rating'.format(HOSTNAME)
    data = {'user_id': user_id, 'movie_id': movie_id, 'rating': rating}
    res = requests.post(url=url, data=data)
    return JsonResponse({})
