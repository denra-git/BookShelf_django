from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book


class BookAccessTests(TestCase):
    
    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse('books:user_book')) 
        self.assertRedirects(response,reverse('users:login')+ '?next=/books/',status_code=302)


    def test_authenticated_user_can_access_books(self):
        user = User.objects.create_user(username='aaa',password="aaa258")
        self.client.force_login(user)
        response = self.client.get(reverse('books:user_book'))
        self.assertEqual(response.status_code,200)
      
        
    def test_user_cannot_edit_other_user_book(self):
        user_a = User.objects.create_user(username='a',password='passa123')
        user_b = User.objects.create_user(username='b',password='passb123')
        
        book = Book.objects.create(title='book_title',author='author',owner=user_b)
        
        self.client.force_login(user_a)
        response = self.client.get(reverse('books:edit_book', kwargs={'id':book.id}))
        
        self.assertRedirects(response,reverse('books:user_book'),status_code=302)
        
     
    def test_user_cannot_delete_other_user_book(self):
        user_a = User.objects.create_user(username='a',password='passa123')
        user_b = User.objects.create_user(username='b',password='passb123')
        
        book = Book.objects.create(title='book_title',author='author',owner=user_b)
        
        self.client.force_login(user_a)
        response = self.client.get(reverse('books:delete_book', kwargs={'id':book.id}))
        
        self.assertRedirects(response,reverse('books:user_book'),status_code=302)  
        
        
    def test_user_can_edit_own_book(self):
            user_a = User.objects.create_user(username='a',password='passa123')
            book = Book.objects.create(title='book_title',author='author',owner=user_a)
            
            self.client.force_login(user_a)
            
            response = self.client.get(reverse('books:edit_book', kwargs={'id':book.id}))
            
            self.assertEqual(response.status_code,200) 
            
            
    def test_user_can_delete_own_book(self):
        user_a = User.objects.create_user(username='a',password='passa123')
        book = Book.objects.create(title='book_title',author='author',owner=user_a)
        
        self.client.force_login(user_a)
        
        response = self.client.post(reverse('books:delete_book', kwargs={'id':book.id}))
        
        self.assertRedirects(response,reverse('books:user_book'),status_code=302) 
        self.assertFalse(Book.objects.filter(id=book.id).exists(),)
        
        
