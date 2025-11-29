# # Import necessary modules for authentication and authorization
# # - render: renders an HTML page based on a template
# # - redirect: redirects to another page
# # - authenticate: checks if a username and password combination is valid
# # - login: logs a user in
# # - logout: logs a user out
# # - login_required: a decorator that checks if a user is logged in
# # - LoginRequiredMixin: a mixin class that checks if a user is logged in
# # - View: a base class for views
# # - User: a model for users
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views import View
# from django.contrib.auth.models import User
# from .forms import RegisterForm

# # Create your views here.

# def register_view(request):
#     # check if the request is POST
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         # check if the form is valid, then create a user
#         if form.is_valid():
#             # get the cleaned data, then create user and login and redirect to homepage
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = User.objects.create_user(username=username, password=password)
#             login(request, user)
#             return redirect('home')
#     else:
#         # if form is not valid, then registeration form
#         form = RegisterForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'accounts/register.html', context)

# def login_view(request):
#     # check if the request is POST
#     if request.method == "POST":
#         # get the username and password from the form
#         username = request.POST['username']
#         password = request.POST['password']
#         # authenticate the user
#         user = authenticate(request, username=username, password=password)
        
#         # if user is authenticated, log them in
#         if user is not None:
#             login(request, user)
#             return redirect(request.GET.get('next', '/'))
#         else:
#             # wrong password/username → show error
#             return render(request, 'accounts/login.html', {
#                 'error': 'Invalid username or password'
#             })
    
#     # This part was missing! → when someone just opens the login page (GET request)
#     else:
#         return render(request, 'accounts/login.html')

# @login_required
# def logout_view(request):
#     if request.method == "POST":
#         logout(request)
#         return redirect('login')
#     return redirect('home_view')


# # home view -- using the decorator
# @login_required
# def home_view(request):
#     return render(request, 'invApp/home.html')


# # protected view

# # class ProtectedView(LoginRequiredMixin, View):
# #     login_url = 'login'
# #     # defualt redirect field = 'next'
# #     redirect_field_name = 'redirect_to'

# #     def get(self, request):
# #         return render(request, 'registration/protected.html')


# Import necessary modules for authentication and authorization
# - render: renders an HTML page based on a template
# - redirect: redirects to another page
# - authenticate: checks if a username and password combination is valid
# - login: logs a user in
# - logout: logs a user out
# - login_required: a decorator that checks if a user is logged in
# - LoginRequiredMixin: a mixin class that checks if a user is logged in
# - View: a base class for views
# - User: a model for users

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User  # (currently unused, but kept if needed later)
from .forms import RegisterForm


def register_view(request):
    """
    Handles user registration using RegisterForm.
    Uses form.save(), which:
    - saves username + email
    - hashes the password with set_password()
    - enforces strong password validation
    - checks password confirmation & unique email
    """
    # Optional: prevent logged-in users from seeing the register page
    if request.user.is_authenticated:
        return redirect('home')  # keep your existing redirect target

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Let the form handle creating the user properly
            user = form.save()
            # Automatically log the user in after successful registration
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    # check if the request is POST
    if request.method == "POST":
        # get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the user
        user = authenticate(request, username=username, password=password)

        # if user is authenticated, log them in
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            # wrong password/username → show error
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    # when someone just opens the login page (GET request)
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('home_view')


# home view -- using the decorator
@login_required
def home_view(request):
    return render(request, 'invApp/home.html')


# Example protected class-based view if you ever need it:

# class ProtectedView(LoginRequiredMixin, View):
#     login_url = 'login'
#     # default redirect field = 'next'
#     redirect_field_name = 'redirect_to'
#
#     def get(self, request):
#         return render(request, 'registration/protected.html')


