from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/",views.signup, name="signup"),
    path("login/",views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('profile/', views.leaderboard_view, name='profile'),

    #Module no . 2 Brain Boost
    path('brainboost/', views.brainboost_home, name='brainboost_home'),
    path('brainboost/<str:category>/', views.brainboost_quiz, name='brainboost_quiz'),
    path('brainboost-results/', views.brainboost_results_admin, name='brainboost_results_admin'),

    #Module no . 3 WordWhiz 
    path('wordwhiz/', views.wordwhiz_home, name='wordwhiz_home'),
    path('wordwhiz/<str:category>/', views.wordwhiz_quiz, name='wordwhiz_quiz'),

    #Module no . 4 MapQuest Mode
    path('mapquest/', views.mapquest_home, name='mapquest_home'),
    path('mapquest/<str:category>/', views.mapquest_quiz, name='mapquest_quiz'),
    path('mapquest-results/', views.mapquest_results_admin, name='mapquest_results_admin'),

    path('download-report/', views.download_weekly_report, name='download_report'),
    path("",views.home, name="home"),
    path('performance/', views.performance_tracker, name='performance_tracker'),
    path('submit-question/', views.submit_question, name='submit_question'),
    path('challenge/', views.challenge_mode, name='challenge_mode'),
    path("redeem/",views.redeem, name="redeem"),
    path("quiz/",views.quiz, name="quiz"),

    #Contact_Us + About_Us
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),

    #Module no . 8 Gamification & Reward System
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('badges/', views.badge_showcase_view, name='badge_showcase'),

]