from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_job, name='add_job'), 
    path('jobs/', views.job_list, name='job_list'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('reminders/', views.send_reminders, name='send_reminders'),
    path('register/', views.register, name='register'), 
]