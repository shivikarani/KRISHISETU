from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

from .models import Article, Category
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

# previous queries

@login_required(login_url='login')
def view_queries(request):
    # Fetch queries submitted by this farmer, newest first
    queries = request.user.query_set.all().order_by('-created_at')
    return render(request, 'core/view_queries.html', {'queries': queries})


# knowledge base view


# def knowledge_base(request):
#     category_id = request.GET.get('category')
#     if category_id:
#         articles = Article.objects.filter(category_id=category_id).order_by('-created_at')
#     else:
#         articles = Article.objects.all().order_by('-created_at')
#     categories = Category.objects.all()
#     return render(request, 'core/knowledge_base.html', {'articles': articles, 'categories': categories})


# creating api


from django.http import JsonResponse
from .models import Article, Category

def articles_api(request):
    category_id = request.GET.get('category')
    
    if category_id:
        articles = Article.objects.filter(category_id=category_id)
    else:
        articles = Article.objects.all()

    data = []
    for article in articles:
        data.append({
            'id': article.id,
            'title': article.title,
            'category': article.category.name,
            'content': article.content[:150],
            'created_at': article.created_at.strftime("%d %b %Y")
        })

    return JsonResponse({'articles': data})


def categories_api(request):
    categories = Category.objects.all()
    data = [{'id': c.id, 'name': c.name} for c in categories]
    return JsonResponse({'categories': data})

@login_required(login_url='login')
def knowledge_base(request):
    return render(request, 'core/knowledge_base.html')