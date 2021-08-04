from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logs/<slug>/', views.LogsView.as_view(), name='logs'),
    path('enter/<slug>/', views.EnterView.as_view(), name='enter'),
    path('enter_done/', views.EnterDoneView.as_view(), name='enter_done'),
    path('exit/<slug>/', views.ExitView.as_view(), name='exit'),
    path('exit_done/', views.ExitDoneView.as_view(), name='exit_done'),
    path('system/', views.SystemView.as_view(), name='system'),
]
