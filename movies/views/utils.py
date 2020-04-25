from django.core.paginator import Paginator
from ..models import Rating
import json



HOSTNAME = '192.168.137.205'
HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
}


movie_data = json.load(open('/home/tupham/web-mining/web_server/dj_review_app/project/movies(1).json', 'r'))

def paginate(request, items, items_per_page):
    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return items


def get_rating(movie):
    vote_count = movie['vote_count']
    vote_average = movie['vote_average']
    user_ratings = Rating.objects.filter(movie=movie['tmdb_id'])
    score = vote_count * vote_average / 2
    for rating in user_ratings:
        score += rating.score
    try:
        score /= (vote_count + len(user_ratings))
    except:
        score = 0

    score = round(score, 1)
    movie['rating'] = score
    movie['vote_count'] += len(user_ratings)
    return movie


def image_placeholder():
    data = movie_data
    backdrop, poster = [], []
    for k, v in movie_data.items():
        if(v['backdrop_path'].find('originalNone') != -1):
            data[k]['backdrop_path'] = 'https://via.placeholder.com/640x360.png?text=Generic+Placeholder+Image'
            backdrop.append(k)
        if(v['poster_path'].find('originalNone') != -1):
            data[k]['poster_path'] = 'https://via.placeholder.com/842x1191.png?text=Generic+Placeholder+Image'
            poster.append(k)

    print(len(backdrop))
    print(len(poster))

    json.dump(data, open('/home/tupham/web-mining/server/dj_review_app/project/movies(1).json', 'w'))


def import_data():
    for tmdb_id, movie in movie_data:
        pass
