from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from algorithims.decoretor import *
from .forms import *


# Create your views here.
#-------------------------------------------------------------


def auto_login(request, username, password, remember=True):
    '''
    Return the user to specific homepage after signup
    '''
    user = authenticate(
        request, username=username,
        password=password, remember=remember)
    if user is not None:
        if user.permision() == 'ad':
            login(request, user)
            # redirect to administrator
            return redirect('/administrator/home')

        elif user.permision() == 'te':
            login(request, user)
            return redirect('/teacher/')

@unauthenticated_administrator
@unauthenticated_teacher
def reset_password(request, *args, **kwargs):
    form = MyCustomResetPasswordForm(request.POST or None)
    if form.is_valid():
        form.save()
        print(form.cleaned_data)

    dt = {
        'reset_password': form,
    }
    return render(request, 'account/password_reset.html', dt)
#==============================================================

@unauthenticated_administrator
@unauthenticated_teacher
def roles_homepage(request, *args, **kwargs):
    '''
    Assigning roles for the users who signed up
    '''
    form = Select(request.POST or None)
    if form.is_valid():
        t = form.cleaned_data['Select_Role']
        if t == 'ad':
            return redirect('/accounts/signup/administrator/')
        else:
            return redirect('/accounts/signup/teacher/')
    dt = {
        'form': form
    }
    return render(request, 'roles_homepage.html', dt)

@unauthenticated_administrator
@unauthenticated_teacher
def signup_page_te(request, *args, **kwargs):
    '''
    For teacher only
    '''
    form = MyCustomSignupForm_te(request.POST or None)
    if form.is_valid():
        form.save(request)
        # redirect to a new URL:
        username = request.POST.get('username')
        password = request.POST.get('password1')
        return auto_login(request=request, password=password, username=username)

    dt = {
        'signup': form,
    }
    return render(request, 'account/signup_te.html', dt)

@unauthenticated_administrator
@unauthenticated_teacher
def signup_page_ad(request, *args, **kwargs):
    '''
    Only for administrator
    '''
    form = MyCustomSignupForm_ad(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save(request)
            # redirect to a new URL:
            username = request.POST.get('username')
            password = request.POST.get('password1')
            return auto_login(request=request, password=password, username=username)

    dt = {
        'signup': form,
    }
    return render(request, 'account/signup_ad.html', dt)


@unauthenticated_administrator
@unauthenticated_teacher
def login_page(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        user = authenticate(
            request, username=username,
            password=password, remember=remember)
        if user is not None:
            if user.permision() == 'ad':
                login(request, user)
                # redirect to administrator
                return redirect('/administrator/home')

            elif user.permision() == 'te':
                login(request, user)
                return redirect('/teacher/')

    form = MyCustomLoginForm(request.POST or None)
    dt = {
        'login': form,
    }
    return render(request, 'account/login.html', dt)

def logout_page(request, *args, **kwargs):
    logout(request)
    return redirect('/accounts/login/')


