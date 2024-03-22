from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib import messages

@login_required(login_url='login_user')
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            try:
                # Attempt to create a new user
                User.objects.create_user(username=uname, email=email, password=pass1)
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login_user')
            except IntegrityError:
                # Handle IntegrityError (e.g., duplicate entry) gracefully
                return HttpResponse("An error occurred while creating the user. Please try again.")

    return render(request, 'register.html')

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
    else:
        # Render the login form for GET requests
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('login_user')
