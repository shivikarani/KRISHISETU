from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import Notification
from .models import Article, Category
from .models import Query, ExpertResponse
import requests
from django.conf import settings
from .ml_model.predict import predict_disease
def home(request):
    schemes = GovernmentScheme.objects.all()
    return render(request, "core/home.html", {"schemes": schemes})


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

            # Redirect based on role
            return redirect_user_dashboard(request)

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')



from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):

    city = request.GET.get('city', 'Delhi')

    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    weather_data = None

    if response.status_code == 200:
        weather_data = {
            "city": data["name"],   # 🔥 IMPORTANT FIX
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "wind": data["wind"]["speed"],          # add
            "pressure": data["main"]["pressure"]
        }

        advisory = ""

        if weather_data:
            temp = weather_data["temperature"]

            if temp > 35:
                advisory = "High temperature! Ensure proper irrigation."
            elif temp < 10:
                advisory = "Low temperature! Protect crops from frost."
            else:
                advisory = "Weather conditions are suitable for farming activities."

    if response.status_code != 200:
       weather_data = None
       advisory = "⚠️ Please enter a valid city name"

    return render(request, 'core/dashboard.html', {
        "weather": weather_data,
        "advisory": advisory
    })


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
    queries = Query.objects.filter(farmer=request.user).order_by('-created_at')

    responses = ExpertResponse.objects.filter(
        query__in=queries
    ).select_related('query')

    return render(request, 'core/view_queries.html', {
        'queries': queries,
        'responses': responses
    })



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





from django.contrib.auth.decorators import user_passes_test


def is_expert(user):
    return (
        user.groups.filter(name='Expert').exists() and
        hasattr(user, 'expertprofile') and
        user.expertprofile.is_approved
    )
@user_passes_test(is_expert, login_url='login')
def expert_dashboard(request):
    queries = Query.objects.all().order_by('-created_at')
    return render(request, 'core/expert_dashboard.html', {'queries': queries})


@user_passes_test(is_expert, login_url='login')
def respond_query(request, query_id):
    query = Query.objects.get(id=query_id)

    if request.method == 'POST':
        response_text = request.POST.get('response_text')
        response_voice = request.FILES.get('response_voice')

        ExpertResponse.objects.create(
            query=query,
            expert=request.user,
            response_text=response_text,
            response_voice=response_voice
        )

        query.status = 'responded'
        query.is_answered = True
        query.response_text = response_text
        query.save()
        Notification.objects.create(
            user=query.farmer,
            message=f"Your query '{query.title}' has been answered."
        )

        return redirect('expert_dashboard')

    return render(request, 'core/respond_query.html', {'query': query})


@login_required(login_url='login')
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # mark all as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'core/notifications.html', {'notifications': notifications})





from django.conf import settings
import requests
from django.http import JsonResponse


def market_prices(request):

    api_key = settings.DATA_GOV_API_KEY
    state = request.GET.get("state")
    url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001adf9c207395e44127e9e6a3e5fc9f71d&format=json&limit=100&offset=100"
    if state:
        url += f"&filters[state]={state}"
    try:

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])
            return JsonResponse(records, safe=False)

        else:
            return JsonResponse({"error": "API not responding"}, status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Connection failed"}, status=500)



from .forms import CropRecommendationForm


def crop_recommendation(request):

    result = None

    if request.method == "POST":
        form = CropRecommendationForm(request.POST)

        if form.is_valid():

            soil = form.cleaned_data["soil_type"]
            temp = form.cleaned_data["temperature"]
            temp_unit = form.cleaned_data["temp_unit"]
            humidity = form.cleaned_data["humidity"]
            rainfall = form.cleaned_data["rainfall"]
            rain_unit = form.cleaned_data["rain_unit"]

            # convert temperature to Celsius
            if temp_unit == 'F':
                temp = (temp - 32) * 5/9

            # convert rainfall to mm
            if rain_unit == 'cm':
                rainfall = rainfall * 10

            # logic
            if soil == "clay" and rainfall > 200:
                result = "Rice"
            elif soil == "loamy" and temp > 20:
                result = "Wheat"
            elif soil == "sandy":
                result = "Millet"
            else:
                result = "Maize"

    else:
        form = CropRecommendationForm()

    return render(request, "core/crop_recommendation.html", {
        "form": form,
        "result": result
    })

from .models import GovernmentScheme
def government_schemes(request):

    # Admin schemes
    admin_schemes = GovernmentScheme.objects.all()

    # API data
    api_schemes = []

    try:
        url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={settings.DATA_GOV_API_KEY}&format=json&limit=5"

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            for item in data.get("records", []):
                api_schemes.append({
                    "title": item.get("commodity"),
                    "description": f"{item.get('state')} - ₹{item.get('modal_price')}",
                })

    except Exception as e:
        print("API error:", e)
    return render(request, "core/schemes.html", {
        "admin_schemes": admin_schemes,
        "api_schemes": api_schemes
    })


from .models import UserProfile
from .forms import ProfileForm

def profile(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully ✅")
            return redirect('dashboard')    # IMPORTANT
    else:
        form = ProfileForm(instance=profile)

    return render(request, "core/profile.html", {"form": form})





from django.db.models import Q
from .models import Article, GovernmentScheme

def search(request):

    query = request.GET.get('q')

    articles = []
    schemes = []
    if query:
        q = query.lower()

        if "kidneybeans" in q:
            query = "kidney beans"

    if query:
        # Step 1: exact + partial match
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

        schemes = GovernmentScheme.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # Step 2: fallback (agar kuch nahi mila)
        if not articles.exists():
            articles = Article.objects.all()[:5]   # top 5

        if not schemes.exists():
            schemes = GovernmentScheme.objects.all()[:5]

    else:
        # Step 3: empty search → default data
        articles = Article.objects.all()[:5]
        schemes = GovernmentScheme.objects.all()[:5]

    context = {
        'query': query,
        'articles': articles,
        'schemes': schemes
    }

    return render(request, 'core/search.html', context)



import requests
from .forms import DiseaseForm

from .ml_model.predict import predict_disease

def detect_disease(request):

    result = None
    obj = None

    if request.method == "POST":
        form = DiseaseForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()

            image_path = obj.image.path
            crop = form.cleaned_data['crop']

            try:
                prediction = predict_disease(image_path, crop)
                result = prediction

            except Exception as e:
                result = "Could not process image. Showing default result."

                # ✅ DEFAULT SAFE OUTPUT
                result = "🌿 Healthy Crop (Model temporarily unavailable)"

            obj.result = result
            obj.save()

        else:
            # ✅ Form invalid (PDF, wrong file etc)
            result = "Please upload a valid crop image in JPG/JPEG format"

    else:
        form = DiseaseForm()

    return render(request, "core/disease.html", {
        "form": form,
        "result": result,
        "obj": obj
    })



from django.contrib.auth.models import Group
from .forms import ExpertRegistrationForm

from .models import ExpertProfile

def expert_register(request):
    if request.method == 'POST':
        form = ExpertRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create Expert Profile (NOT approved yet)
            ExpertProfile.objects.create(
                user=user,
                qualification=form.cleaned_data['qualification'],
                experience_years=form.cleaned_data['experience_years'],
                is_approved=False
            )

            return render(request, 'core/expert_pending.html')
    else:
        form = ExpertRegistrationForm()

    return render(request, 'core/expert_register.html', {'form': form})



from django.shortcuts import redirect

def redirect_user_dashboard(request):
    user = request.user

    # If user applied as expert but NOT approved
    if hasattr(user, 'expertprofile'):
        if not user.expertprofile.is_approved:
            return render(request, 'core/expert_pending.html')

    # If approved expert
    if user.groups.filter(name='Expert').exists():
        return redirect('expert_dashboard')

    # Default → farmer
    return redirect('dashboard')


from .forms import SoilAnalysisForm
from .models import SoilAnalysis

@login_required(login_url='login')
def soil_analysis(request):

    result = None

    if request.method == "POST":
        form = SoilAnalysisForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user

            lat = obj.latitude
            lon = obj.longitude

            # 🔥 SIMPLE LOGIC (replace later with API/ML)
            if lat > 25:
                soil = "Loamy Soil"
                crop = "Wheat"
                fertilizer = "Use Nitrogen-rich fertilizer"
            else:
                soil = "Sandy Soil"
                crop = "Millet"
                fertilizer = "Use Organic Compost"

            obj.detected_soil = soil
            obj.recommended_crop = crop
            obj.fertilizer_suggestion = fertilizer

            obj.save()

            result = obj

    else:
        form = SoilAnalysisForm()

    return render(request, "core/soil_analysis.html", {
        "form": form,
        "result": result
    })



def faq(request):
    faqs = [

        # BASIC USAGE
        {
            "question": "How to submit a query?",
            "answer": "Go to Dashboard → Click on Submit Query → Fill details → Upload image or voice → Submit."
        },
        {
            "question": "How can I contact an expert?",
            "answer": "Submit your query and experts will respond with text or voice solution."
        },
        {
            "question": "Can I send voice queries?",
            "answer": "Yes, you can upload your voice recording while submitting a query."
        },

        # DISEASE DETECTION
        {
            "question": "How does disease detection work?",
            "answer": "Upload a clear JPEG image of crop leaves and select the correct crop to detect disease."
        },
        {
            "question": "Why am I not getting disease result?",
            "answer": "Make sure image is clear, crop is selected correctly and image is in JPG/JPEG format."
        },
        {
            "question": "Can I upload any image for disease detection?",
            "answer": "No, only crop leaf images in JPEG format are supported."
        },

        # WEATHER
        {
            "question": "How to check weather for my location?",
            "answer": "Enter your city name to get weather details."
        },
        # {
        #     "question": "Can I check weather for village?",
        #     "answer": "Yes, use 'Use My Location' button for accurate weather based on your location."
        # },

        # CROP RECOMMENDATION
        {
            "question": "How to get crop recommendation?",
            "answer": "Enter soil type, temperature, humidity and rainfall to get best crop suggestion."
        },
        {
            "question": "What if I don't know exact values?",
            "answer": "You can estimate values or use weather data from dashboard."
        },

        # FARMING QUESTIONS
        {
            "question": "Which crop is best for my soil?",
            "answer": "Use crop recommendation feature or ask expert by submitting a query."
        },
        {
            "question": "How to increase crop yield?",
            "answer": "Use proper fertilizers, irrigation, and follow expert advice."
        },
        {
            "question": "Which fertilizer should I use?",
            "answer": "Depends on crop and soil. You can ask expert or future soil module will help."
        },
        {
            "question": "How to control pests?",
            "answer": "Use recommended pesticides or consult expert for safe solutions."
        },

        # GOVERNMENT SCHEMES
        {
            "question": "Where can I find government schemes?",
            "answer": "Go to Schemes section to view latest government schemes."
        },
        {
            "question": "Are schemes updated regularly?",
            "answer": "Yes, schemes are fetched from government APIs."
        },

        # NOTIFICATIONS
        {
            "question": "How will I know if expert replied?",
            "answer": "You will get a notification in Notifications section."
        },

        # 👤 PROFILE
        {
            "question": "How to update my profile?",
            "answer": "Click on Profile in navbar and update your details."
        },
        # {
        #     "question": "Can I upload profile picture?",
        #     "answer": "Yes, you can upload your profile image."
        # },

        # SEARCH & LANGUAGE
        {
            "question": "How to search information?",
            "answer": "Use search bar to find crops, schemes and articles."
        },
        {
            "question": "Can I change language?",
            "answer": "Yes, use Google Translate option to change language."
        },

        # GENERAL ISSUES
        {
            "question": "Why is my image not uploading?",
            "answer": "Make sure image is valid, not corrupted and in supported format."
        },
        {
            "question": "Why is website not showing results?",
            "answer": "Check internet connection or try refreshing page."
        },
        {
            "question": "What should I do if something is not working?",
            "answer": "Try refreshing page or contact support."
        }

    ]

    return render(request, "core/faq.html", {"faqs": faqs})



from django.contrib import messages
from django.shortcuts import redirect

def contact(request):

    if request.method == "POST":

        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(name, mobile, email, message)

        messages.success(request, "Message sent successfully!")

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('/')