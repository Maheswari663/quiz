from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('student/login/', views.student_login, name='student_login'),
   path('student/register/',views.student_register, name='student_register'),
    path('logout/', views.logout_view, name='logout'),
]
