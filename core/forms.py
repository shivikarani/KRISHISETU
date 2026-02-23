from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class FarmerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    state = forms.CharField(max_length=100)
    district = forms.CharField(max_length=100)
    village = forms.CharField(max_length=100)
    crop_types = forms.CharField(max_length=200)
    land_size = forms.FloatField()
    preferred_language = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'state', 'district', 'village', 'crop_types', 'land_size', 'preferred_language']


        # query submission form

from .models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['title', 'description', 'crop_type', 'media_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }