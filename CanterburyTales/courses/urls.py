from django.urls import path

from CanterburyTales.courses import views

app_name = 'courses'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # ALL POSSIBLE INDEX URLS
    path('search/audience/<str:audience>/<int:audience_exact>/tags/<str:tags>/<int:tags_exact>/', views.IndexView.as_view(),
         name='index_full_search'),
    path('search/audience/<str:audience>/<int:audience_exact>/tags/<str:tags>/', views.IndexView.as_view(),
         name='index_search_1'),
    path('search/audience/<str:audience>/tags/<str:tags>/<int:tags_exact>/', views.IndexView.as_view(),
         name='index_full_search_2'),
    path('search/audience/<str:audience>/tags/<str:tags>/', views.IndexView.as_view(), name='index_full_search_3'),
    path('search/audience/<str:audience>/<int:audience_exact>/', views.IndexView.as_view(), name='index_audience_search'),
    path('search/audience/<str:audience>/', views.IndexView.as_view(), name='index_audience_search'),
    path('search/tags/<str:tags>/<int:tags_exact>/', views.IndexView.as_view(), name='index_tag_search'),
    path('search/tags/<str:tags>/', views.IndexView.as_view(), name='index_tag_search'),


    # handle other urls
    path('courses/create/', views.CourseCreate.as_view(), name='create'),
    path('courses/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('courses/<int:pk>/edit', views.CourseUpdate.as_view(), name='edit'),
    path('courses/upvote/<int:pk>/', views.course_upvote, name='upvote'),
    path('courses/addDownload/<int:pk>/', views.course_add_download, name='add_download'),
    path('courses/<int:pk>/delete/', views.course_delete, name='delete'),
    path('courses/<int:c_id>/newFile/', views.add_file, name='add_file'),
    path('courses/<int:c_id>/deleteFile/<int:f_id>/', views.delete_file, name='delete_file'),

]
