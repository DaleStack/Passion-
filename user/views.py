from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserModel
from .forms import UserRegister, UserLogin
from django.contrib.auth import authenticate, login, logout
# Create your views here.

#USER REGISTRATION
def register_view(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # Save the user object
                login(request, user)  # Log the user in immediately after registration
                messages.success(request, 'Registration successful!')
                
                # Check if the user is a teacher or student
                if form.cleaned_data['role'] == UserModel.BUYER:
                    return redirect('buyer_dashboard')  # Redirect to buyer dashboard
                else:
                    return redirect('seller_dashboard')  # Redirect to seller dashboard
            except Exception as e:
                print(f"Error during registration: {e}")
                messages.error(request, 'Oops! Something went wrong.')
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        form = UserRegister()

    return render(request, 'user/register.html', {'form': form})

#USER LOGIN
def login_view(request):
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back!')

                # Redirect based on the role
                if user.is_buyer():
                    return redirect('buyer_dashboard')  # Redirect to teacher dashboard
                else:
                    return redirect('seller_dashboard')  # Redirect to student dashboard
            else:
                messages.error(request, 'Invalid credentials, please try again.')
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        form = UserLogin()

    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

        

