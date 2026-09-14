from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    cover = models.ImageField(upload_to="book_covers/",blank=True,null=True)
