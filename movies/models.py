from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=200)
    overview = models.CharField(max_length=500)
    release_date = models.DateField(null=True, blank=True)
    poster_path = models.URLField()
    backdrop_path = models.URLField()
    training_vote_count = models.IntegerField(default=0)
    training_avg_score = models.FloatField(default=0)

    def __str__(self):
        return str(self.__dict__)

class Rating(models.Model):
    SCORES = [
        (5, 5),
        (4, 4),
        (3, 3),
        (2, 2),
        (1, 1),
    ]
    score = models.IntegerField(choices=SCORES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='ratings',on_delete=models.CASCADE)
    movie = models.CharField(max_length=10)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, related_name='genres', on_delete=models.CASCADE)

