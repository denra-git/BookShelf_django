from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.storage.base import Message
from django.contrib.messages.test import MessagesTestMixin
from .models import Book,Category


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
        user = User.objects.create_user(username='a',password='passa123')
        book = Book.objects.create(title='book_title',author='author',owner=user)
        
        self.client.force_login(user)
        
        response = self.client.get(reverse('books:edit_book', kwargs={'id':book.id}))
        
        self.assertEqual(response.status_code,200) 
            
            
    def test_user_can_delete_own_book(self):
        user = User.objects.create_user(username='a',password='passa123')
        book = Book.objects.create(title='book_title',author='author',owner=user)
        
        self.client.force_login(user)
        
        response = self.client.post(reverse('books:delete_book', kwargs={'id':book.id}))
        
        self.assertRedirects(response,reverse('books:user_book'),status_code=302) 
        self.assertFalse(Book.objects.filter(id=book.id).exists(),)
        
  
        
class BookRelationshipTests(TestCase):
    
    def test_correct_owner(self):
        
        user = User.objects.create_user(username='a',password='passa123')
        book = Book.objects.create(title='title',author='author',owner=user)
        
        self.assertEqual(user,book.owner)
        
    
    def test_many_to_many_relationship(self):
        
        user = User.objects.create_user(username='a',password='passa123')
        book = Book.objects.create(title='title',author='author',owner=user)
        category_1 =Category.objects.create(name='novel')
        category_2 =Category.objects.create(name='poetry')
        
        book.categories.add(category_1,category_2)
        
        self.assertIn(category_1,book.categories.all())
        self.assertIn(category_2,book.categories.all())
 
    
    
class BookMessageTests(MessagesTestMixin, TestCase):
    
        def setUp(self):
            self.user = User.objects.create_user(username='a')
            self.book = Book.objects.create(title='title',author='author',owner=self.user)
        
        
        def test_add_book_success_message(self):
            self.client.force_login(self.user)
            response = self.client.post(reverse('books:add_book'),{'title':'title','author':'author'})

            expected_messages = [Message(messages.SUCCESS, ". SUCCESSFULLY ADDED .")]

            self.assertRedirects(response,reverse('books:user_book'),status_code=302)
            self.assertMessages(response, expected_messages, ordered=True)
        
        
        def test_edit_book_success_message(self):
                
            self.client.force_login(self.user)
            
            response = self.client.post(reverse('books:edit_book',kwargs={'id':self.book.id}),{'title': 'title_edited','author':'author'})
            
            expected_messages = [Message(messages.SUCCESS, ". SUCCESSFULLY EDITED .")]
            
            self.book.refresh_from_db()
            
            self.assertRedirects(response,reverse('books:book_detail',kwargs={'id': self.book.id}),status_code=302)
            self.assertEqual(self.book.title,'title_edited')
            self.assertMessages(response, expected_messages, ordered=True)
         
                    
        def test_delete_book_success_message(self):
            
            self.client.force_login(self.user)
            
            response = self.client.post(reverse('books:delete_book',kwargs={'id':self.book.id}))
            
            expected_messages = [Message(messages.SUCCESS,". SUCCESSFULLY DELETED .")]
            
            self.assertRedirects(response,reverse('books:user_book'),status_code=302)
            self.assertFalse(Book.objects.filter(id=self.book.id).exists())
            self.assertMessages(response, expected_messages, ordered=True)
            
                
                
class BookErrorTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='a')


    def test_nonexistent_book_detail_id_returns_404(self):
        
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('books:book_detail',kwargs={'id':313313313}))
        
        self.assertEqual(response.status_code,404)
        
    
    def test_nonexistent_book_edit_id_returns_404(self):
        
        self.client.force_login(self.user)
            
        response = self.client.get(reverse('books:edit_book',kwargs={'id':313313313}))
        
        self.assertEqual(response.status_code,404)
        
        
    def test_nonexistent_book_delete_id_returns_404(self):
        
        self.client.force_login(self.user)
            
        response = self.client.get(reverse('books:delete_book',kwargs={'id':313313313}))
        
        self.assertEqual(response.status_code,404)
        
        
        
class BookCRUDTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='a')
        self.book = Book.objects.create(title='title',author='author',owner=self.user)
        
    
    def test_add_book(self):
        
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('books:add_book'),{'title':'title','author':'author'})
        
        book = Book.objects.filter(title='title',owner=self.user)
        
        self.assertRedirects(response,reverse('books:user_book'),status_code=302)
        self.assertTrue(book.exists())
        
    
    def test_read_book_detail(self):
        
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('books:book_detail',kwargs={'id':self.book.id}))
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.book , response.context['book'])
        
        
    def test_updating_book(self):
        
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('books:edit_book',kwargs={'id':self.book.id}),{'title':'new_title','author':'author'})
        
        self.book.refresh_from_db()
        
        self.assertRedirects(response,reverse('books:book_detail',kwargs={'id':self.book.id}))
        self.assertEqual(self.book.title ,'new_title' )
       
        
    def test_delete_book(self):
        
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('books:delete_book',kwargs={'id': self.book.id}))
        
        self.assertRedirects(response,reverse('books:user_book'),status_code=302)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())