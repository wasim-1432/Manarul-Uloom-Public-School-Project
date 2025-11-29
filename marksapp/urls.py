# marksapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.enter_roll, name='enter_roll'),
]