from django.urls import path

from CanterburyTales.courses import views

app_name = 'courses'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # ALL POSSIBLE INDEX URLS
    path('search/audience/<str:audience>/<int:audience_exact>/tags/<str:tags>/<int:tags_exact>/', views.IndexView.as_view(),
         name='index_full_search'),
    path('search/audience/<str:audience>/<int:audience_exact>/tags/<str:tags>/', views.IndexView.as_view(), name='index_full_search'),
    path('search/audience/<str:audience>/tags/<str:tags>/<int:tags_exact>/', views.IndexView.as_view(),
         name='index_full_search'),
    path('search/audience/<str:audience>/tags/<str:tags>/', views.IndexView.as_view(), name='index_full_search'),
    path('search/audience/<str:audience>/<int:audience_exact>/', views.IndexView.as_view(), name='index_audience_search'),
    path('search/audience/<str:audience>/', views.IndexView.as_view(), name='index_audience_search'),
    path('search/tags/<str:tags>/<int:tags_exact>/', views.IndexView.as_view(), name='index_tag_search'),
    path('search/tags/<str:tags>/', views.IndexView.as_view(), name='index_tag_search'),

    path('courses/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('courses/create/', views.CourseCreate.as_view(), name='create'),
    path('courses/upvote/<int:pk>/', views.course_upvote, name='upvote')
]
