from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('',views.user_book,name='user_book'),
    path('add_book/',views.add_book,name='add_book'),
    path('edit/<int:id>',views.edit_book,name='edit_book'),
    path('detail/<int:id>',views.book_detail,name='book_detail'),
    path('delete/<int:id>',views.delete_book,name='delete_book')
]