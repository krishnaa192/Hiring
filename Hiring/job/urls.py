
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name='home'),
    path('welcome/', views.welcome, name='welcome'),
    path('signup/', views.candidate_signup, name='signup'),
    path('login/', views.candidate_login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('candidate_profile/', views.candidate_profile, name='candidate_profile'),
    path('job_detail/<str:pk>/', views.job_detail, name='job_detail'),
    path('apply_job/<str:pk>/', views.apply_job, name='apply_job'),
    path('verify/', views.verifications_job, name='verifications_job'),
    path('about/', views.about, name='about'),

   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)