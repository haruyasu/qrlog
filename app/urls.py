from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('enter/', views.EnterView.as_view(), name='enter'),
    path('exit/', views.ExitView.as_view(), name='exit'),
    path('system/', views.SystemView.as_view(), name='system'),
]
