from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import login_required

@login_required
def user_book(request):
    books = Book.objects.filter(owner=request.user)
    return render(request,'books/user_books.html',{'books' : books})
