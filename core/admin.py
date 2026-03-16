from django.contrib import admin
from .models import Category, Article

admin.site.register(Category)
admin.site.register(Article)

from .models import CropRecommendation

admin.site.register(CropRecommendation)


from .models import GovernmentScheme

admin.site.register(GovernmentScheme)




from .models import DiseaseDetection

admin.site.register(DiseaseDetection)