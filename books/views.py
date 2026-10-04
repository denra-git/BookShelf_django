from django.views.generic import DetailView,CreateView,DeleteView,UpdateView,ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse

from .models import Book
from .forms import BookForm


class BookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'books/user_books.html'
    context_object_name = "books"
    
    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user).order_by('-id')
 


class BookCreateView(LoginRequiredMixin,CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/add_form.html"
    success_url = reverse_lazy('books:user_book')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, ". SUCCESSFULLY ADDED .")
        return super().form_valid(form)
    
    
 
class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_form.html'
    
    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)
    
    def get_success_url(self):
        return reverse(
            "books:book_detail",
            kwargs={"pk": self.object.pk},
        )
    
    def form_valid(self, form):
        messages.success(
            self.request,
            ". SUCCESSFULLY EDITED ."
        )
        return super().form_valid(form)



class BookDeleteView(LoginRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books:user_book')
    http_method_names = ["post"]
    
    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)    
    
    def form_valid(self,form):        
        response = super().form_valid(form)
        messages.success(self.request, ". SUCCESSFULLY DELETED .")
        return response
        


class BookDetailView(LoginRequiredMixin,DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)