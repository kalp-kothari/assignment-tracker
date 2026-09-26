from django.urls import path

from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('add/', views.assignment_create, name='assignment_create'),
    path('<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    path('<int:pk>/toggle/', views.assignment_toggle, name='assignment_toggle'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
