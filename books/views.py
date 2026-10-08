from django.views.generic import DetailView,CreateView,DeleteView,UpdateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy,reverse

from .models import Book,Category
from .forms import BookForm


class BookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'books/user_books.html'
    context_object_name = "books"
    paginate_by = 10
    
    def get_queryset(self):
        books = Book.objects.filter(owner=self.request.user)
        
        search =  self.request.GET.get("search")
        if search:
            books = books.filter(Q (title__icontains=search) | 
                         Q (author__icontains=search))
            
        category = self.request.GET.get("category")
        if category:
            books = books.filter(categories__id=category)
            
        sort = self.request.GET.get('sort','-id')
        allowed_sorts = ["-id", "id", "title", "-title"]
        if sort not in allowed_sorts :
            sort = '-id'
            
        return books.order_by(sort)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
 


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