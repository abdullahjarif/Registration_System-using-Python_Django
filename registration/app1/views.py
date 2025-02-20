from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='login')
def HomePage(request):
    return render(request, 'homepage.html')


def Signup_Page(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_pass')

        
        if password != confirm_pass:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('signup')

       
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken! Choose a different one.")
            return redirect('signup')

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered! Use a different one.")
            return redirect('signup')

      
        my_user = User.objects.create_user(username=uname, email=email, password=password)
        my_user.save()

        
        login(request, my_user)

        messages.success(request, "Account created successfully! You are now logged in.")
        return redirect('homepage')  

    return render(request, 'signup.html')


def Login_Page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')


def Logout_Page(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')
