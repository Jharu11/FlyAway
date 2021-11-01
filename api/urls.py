from django.urls import path
from .import views as assets


urlpatterns = [
    path('airports', assets.api, name="api"),    
]
