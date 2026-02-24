from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit-query/', views.submit_query, name='submit_query'),
    path('my-queries/', views.view_queries, name='view_queries'),
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
    path('api/categories/', views.categories_api, name='categories_api'),
    path('api/articles/', views.articles_api, name='articles_api'),
    path('expert-dashboard/', views.expert_dashboard, name='expert_dashboard'),
    path('respond/<int:query_id>/', views.respond_query, name='respond_query'),
    path('notifications/', views.notifications_view, name='notifications'),
]