from django.shortcuts import render,redirect
from .models import Book
from django.contrib.auth.decorators import login_required
from .forms import BookForm


@login_required
def user_book(request):
    books = Book.objects.filter(owner=request.user)
    return render(request,'books/user_books.html',{'books' : books})

@login_required
def add_book(request):
        
    if request.method == 'POST' :
        
        form = BookForm(request.POST)
 
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('books:user_book')
        
    else:
        form = BookForm()
        
    books = Book.objects.filter(owner = request.user).order_by("-id")
    return render(request,"books/add_form.html",{"form" :form})  

@login_required
def edit_book(request):
    book = Book.objects.get(id=book_id)
    if book.owner == request.user:
        #edit the book
        pass
    else:
        pass
    

@login_required
def delete_book(request):
    book = Book.objects.get(id=book_id)
    if book.owner == request.user:
        #delete the book
        pass
    else:
            pass