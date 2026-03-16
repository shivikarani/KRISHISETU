from django.db import models
from django.contrib.auth.models import User


# =========================
# QUERY MODEL
# =========================

class Query(models.Model):
    QUERY_STATUS = [
        ('submitted', 'Submitted'),
        ('assigned', 'Assigned'),
        ('in_review', 'In Review'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='query_images/', null=True, blank=True)
    voice_file = models.FileField(upload_to='query_voice/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=QUERY_STATUS, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    response_text = models.TextField(blank=True, null=True)
    response_file = models.FileField(upload_to='responses/', blank=True, null=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# =========================
# KNOWLEDGE BASE MODELS
# =========================

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    media_file = models.FileField(upload_to='article/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# EXPERT RESPONSE MODEL
# =========================

class ExpertResponse(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = models.TextField()
    response_voice = models.FileField(upload_to='expert_voice/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.query.title}"
    

    # notification module


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



class MarketPrice(models.Model):
    crop_name = models.CharField(max_length=100)
    mandi = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    min_price = models.FloatField()
    max_price = models.FloatField()
    modal_price = models.FloatField()
    arrival_date = models.DateField()

    def __str__(self):
        return f"{self.crop_name} - {self.mandi}"
    

class CropRecommendation(models.Model):

    SOIL_TYPES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy')
    ]

    soil_type = models.CharField(max_length=50, choices=SOIL_TYPES)
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()

    recommended_crop = models.CharField(max_length=100)

    def __str__(self):
        return self.recommended_crop
    

class GovernmentScheme(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField()
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    state = models.CharField(max_length=100, blank=True, default="")
    district = models.CharField(max_length=100, blank=True, default="")
    village = models.CharField(max_length=100, blank=True, default="")

    crop_type = models.CharField(max_length=100, blank=True, default="")
    land_size = models.FloatField(null=True, blank=True)

    preferred_language = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return self.user.username
    


class DiseaseDetection(models.Model):
    image = models.ImageField(upload_to='diseases/')
    result = models.TextField(blank=True)

    def __str__(self):
        return self.result or "No result"
