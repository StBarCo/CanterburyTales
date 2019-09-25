# profile/urls.py
from django.urls import path

from CanterburyTales.profiles import views

app_name = 'profile'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('<slug:slug>/', views.MyProfileView.as_view(), name='my_profile')
]
