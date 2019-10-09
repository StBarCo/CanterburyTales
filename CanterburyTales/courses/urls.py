from django.urls import path

from CanterburyTales.courses import views

app_name = 'courses'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('courses/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('courses/create/', views.CourseCreate.as_view(), name='create'),
    path('courses/upvote/<int:pk>/', views.course_upvote, name='upvote')
]



