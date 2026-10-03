from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
 

class UserLogicTest(TestCase):
    
    def test_login_completion(self):
        user = User.objects.create_user(username='a',password='a123')
        
        response = self.client.post(reverse('users:login'),{"username":'a',"password":'a123'})
        
        self.assertRedirects(response,reverse('users:profile'),status_code=302)
        self.assertTrue(self.client.session.get('_auth_user_id'))
        
        
    def test_logout_completion(self):
        user = User.objects.create_user(username='a',password='a123')
        self.client.force_login(user)
        
        response = self.client.get(reverse('users:logout'))
        
        self.assertRedirects(response,reverse('users:login'),status_code=302)
        self.assertFalse(self.client.session.get('_auth_user_id'))
        
        
    def test_is_user_registered(self):
        username = 'denra'
        password1 = 'dnr@@258'
        password2 = 'dnr@@258'
        
        response = self.client.post(reverse('users:register'),{'username':username,'password1':password1,'password2':password2})
        
        user = User.objects.filter(username=username)
        
        self.assertRedirects(response,reverse('users:profile'),status_code=302)
        self.assertTrue(user.exists())
        