from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm
# Create your views here.
def index(request):
    """return index.html"""
    return render(request, "index.html")

@login_required

def logout(request):
    """log user out"""
    auth.logout(request)
    messages.success(request, "You have succesfully been logged out")
    return redirect(reverse('index'))

def login(request):
    """log in"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have succesfully logged in")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Your username or password is incorrect")
    else:
        login_form = UserLoginForm()
    # auth.logout(request)
    # messages.success(request, "You have succesfully been logged out")
    return render(request, 'login.html', {'login_form': login_form})

def registration(request):  
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You succesfully registered")
                return redirect(reverse('index'))
            else:
                messages.error(request, "unable to register")   
    else:
        register_form = UserRegistrationForm()
    return render(request, 'registration.html', 
            {'register_form': register_form})

def profile(request):
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {'profile': user})

def accounts(request):
    users = User.objects.all()
    return render(request, "accounts.html", {'users': users})