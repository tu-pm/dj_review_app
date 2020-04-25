from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .utils import movie_data, paginate, get_rating, HOSTNAME, HEADERS
import requests, json


def add_new_user(user_id):
    url='http://{}:8000/add_user?user_id={}'.format(HOSTNAME, user_id)
    print(requests.get(url=url))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            add_new_user(user.id)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
