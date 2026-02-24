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