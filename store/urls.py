from django.urls import path, include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('listing', views.ListView.as_view(), name='listing'),
    path('detail/<int:id>/',views.detail, name='detail'),
    path('search/', views.search, name='search'),
    
]
