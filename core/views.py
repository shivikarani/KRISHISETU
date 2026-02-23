from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'core/home.html')


from django.shortcuts import render, redirect
from .forms import FarmerRegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
    else:
        form = FarmerRegistrationForm()
    return render(request, 'core/register.html', {'form': form})



 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')



from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'core/dashboard.html')


# query submission

from .forms import QueryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def submit_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        if form.is_valid():
            query = form.save(commit=False)
            query.farmer = request.user
            query.save()
            messages.success(request, 'Your query has been submitted!')
            return redirect('dashboard')
    else:
        form = QueryForm()
    return render(request, 'core/submit_query.html', {'form': form})