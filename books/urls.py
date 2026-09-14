from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('user_book/',views.user_book,name='user_book')
]