from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def register(request):
    
    if request.method == 'GET':
        
        form = RegistrationForm()
        return render(request,'users/register.html',{'form': form})
    
    else:
        
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('user_books')
        
        return render(request, 'users/register.html', {'form': form})
    
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        print(user)
        
        if user is not None:
            login(request,user)
            return redirect('users:profile')
           
    return render(request,"users/login.html")


@login_required
def logout_view(requset):
    if requset.method == 'POST':
        logout(requset)
        return redirect('users:login')
    
    
@login_required
def profile(request):
     return render(request,'users/profile.html')
    
 