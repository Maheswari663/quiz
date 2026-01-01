from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

    #dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('my_results/', views.my_results, name='my_results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('settings/', views.settings, name='settings'),
]