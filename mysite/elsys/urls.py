from django.urls import include, path
from elsys import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('cars', views.cars),
    path('commuters', views.commuters)
]
