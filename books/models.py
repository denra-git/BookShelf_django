from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="book_covers/" , blank=True , null=True)
    categories = models.ManyToManyField(Category , blank=True)
    
    def __str__(self):
        return self.title
    

class Review(models.Model):
    description = models.TextField(max_length=1000)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField()
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)