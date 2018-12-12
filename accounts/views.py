from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

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

def SignIn(request):
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
    return render(request, 'SignIn.html', {'login_form': login_form})

def registration(request):  
    # if request.user.is_authenticated:
    #     return redirect(reverse('index'))
    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = True
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('signup.html', {
                'user':user, 
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'We have created an new Commonhold account for you, please activate'
            to_email = register_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect(reverse('accounts'))
    else:
        register_form = UserRegistrationForm()
    return render(request, 'registration.html', 
            {'register_form': register_form})

def profile(request):
    user = User.objects.get(email=request.user.email)
    return render(request, 'profile.html', {'profile': user})

def accounts(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        fields = User._meta.fields
        return render(request, "accounts.html", {'users': users, 'fields': fields})
    else:
        return redirect(reverse('index'))

