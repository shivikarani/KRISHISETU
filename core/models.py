from django.db import models
from django.contrib.auth.models import User

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
    crop_type = models.CharField(max_length=100)
    media_file = models.FileField(upload_to='query_media/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=QUERY_STATUS, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='query_images/', null=True, blank=True) 
    voice_file = models.FileField(upload_to='query_voice/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.farmer.username}"
    
    # knowledge base models

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