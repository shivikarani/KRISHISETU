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

    # ✅ FIXED LAND SIZE (no spinner)
    land_size = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'no-spinner',
            'placeholder': 'Enter land size',
            'step': 'any'
        })
    )

    # ✅ NEW UNIT FIELD
    LAND_UNITS = [
        ('acre', 'Acre'),
        ('hectare', 'Hectare'),
    ]
    land_unit = forms.ChoiceField(choices=LAND_UNITS)

    preferred_language = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'state', 'district', 'village',
            'crop_types', 'land_size', 'land_unit',  # ✅ added
            'preferred_language'
        ]


        # query submission form

from .models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['title', 'description', 'image', 'voice_file']
        






class CropRecommendationForm(forms.Form):

    SOIL_TYPES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy')
    ]

    soil_type = forms.ChoiceField(choices=SOIL_TYPES)

    temperature = forms.FloatField(label="Temperature")
    temp_unit = forms.ChoiceField(choices=[
        ('C', 'Celsius'),
        ('F', 'Fahrenheit')
    ])

    humidity = forms.FloatField(label="Humidity (%)")

    rainfall = forms.FloatField(label="Rainfall")
    rain_unit = forms.ChoiceField(choices=[
        ('mm', 'mm'),
        ('cm', 'cm')
    ])



from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']



from .models import DiseaseDetection


CROP_CHOICES = [
    ('apple', 'Apple'),
    ('tomato', 'Tomato'),
    ('potato', 'Potato'),
    ('corn', 'Corn'),
]

class DiseaseForm(forms.ModelForm):
    crop = forms.ChoiceField(choices=CROP_CHOICES)

    class Meta:
        model = DiseaseDetection
        fields = ['image', 'crop']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            # File type check
            if not image.name.endswith(('.jpg', '.jpeg')):
                raise forms.ValidationError("Only JPG/JPEG images allowed")

            # Optional size limit (5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size should be less than 5MB")

        return image



from django import forms
from django.contrib.auth.models import User

class ExpertRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    qualification = forms.CharField()
    experience_years = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


from .models import SoilAnalysis

class SoilAnalysisForm(forms.ModelForm):
    class Meta:
        model = SoilAnalysis
        fields = ['latitude', 'longitude', 'soil_image']

        

