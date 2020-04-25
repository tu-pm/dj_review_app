from django.urls import path, include
from .views import home, auth, details, trending, history, search

urlpatterns = [
    path('', home.render_template, name='home'),
    path('details/<int:num>', details.render_template, name='details'),
    path('history/', history.render_template, name='history'),
    path('search/', search.render_template, name='search'),
    path('trending/', trending.render_template, name='trending'),
    path('signup/', auth.signup, name='signup'),
    path('add_rating/', details.add_rating, name='add_rating'),
]
