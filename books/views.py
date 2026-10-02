from django.shortcuts import render,redirect
from .models import Book
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.contrib import messages

@login_required
def user_book(request):
    books = Book.objects.filter(owner=request.user)
    return render(request,'books/user_books.html',{'books' : books})
    

@login_required
def add_book(request):
        
    if request.method == 'POST' :
        
        form = BookForm(request.POST,request.FILES)
 
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            form.save_m2m()
            messages.success(request, ". SUCCESSFULLY ADDED .")
            return redirect('books:user_book')
        
    else:
        form = BookForm()
    
    return render(request,"books/add_form.html",{"form" : form})  

@login_required
def edit_book(request,id):
    
    book = Book.objects.get(id=id)
    
    if book.owner != request.user:
         return redirect('books:user_book')
     
    if request.method == 'GET':
        form = BookForm(instance=book)
        return render(request,'books/add_form.html',{'form':form})
        
    else:
        form = BookForm(request.POST,request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, ". SUCCESSFULLY EDITED .")
            return redirect('books:book_detail', id=book.id)
        
        else:
            return render(request,'books/add_form.html',{'form':form})
    

@login_required
def delete_book(request,id):
    
    book = Book.objects.get(id=id)
    
    if book.owner != request.user:
        return redirect('books:user_book')
    
    if request.method == 'POST':   
        book.delete()
        messages.success(request, ". SUCCESSFULLY DELETED .")
        return redirect('books:user_book')
        
        
@login_required        
def book_detail(request,id):
    book = Book.objects.get(id=id)
    
    if book.owner != request.user:
        return redirect('books:user_book')
    
    return render(request,'books/book_detail.html',{'book':book})