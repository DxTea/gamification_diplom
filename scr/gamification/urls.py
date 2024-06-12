from django.urls import path
from .views import *

app_name = 'gamification'
urlpatterns = [
    path('', welcome, name="welcome"),
    path('edit_character/', edit_character, name="edit_character"),
    path('create_character/', create_character, name="create_character"),
    path('deck/', deck, name="deck"),
]
