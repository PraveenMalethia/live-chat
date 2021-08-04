from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('thread/<int:id>/', views.detail, name='detail'),
]
