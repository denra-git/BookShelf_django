from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('',views.BookListView.as_view(),name='user_book'),
    path('detail/<int:pk>/',views.BookDetailView.as_view(),name='book_detail'),
    path('add_book/',views.BookCreateView.as_view(),name='add_book'),
    path('delete/<int:pk>/',views.BookDeleteView.as_view(),name='delete_book'),
    path('edit/<int:pk>/',views.BookUpdateView.as_view(),name='edit_book'),
]