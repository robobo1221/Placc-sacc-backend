from django.urls import path, include
from .views import RegisterAchievementToUser, GetUserAchievements, GetAchievements, GetAchievementId, GetAchievementCode, GetUser, GetUsers

urlpatterns = [
    path('register-achievement', RegisterAchievementToUser.as_view()),
    path('user-achievements', GetUserAchievements.as_view()),
    path('achievements', GetAchievements.as_view()),
    path('achievement/<int:id>', GetAchievementId.as_view()),
    path('achievement-code/<str:code>', GetAchievementCode.as_view()),
    path('user/<str:username>', GetUser.as_view()),
    path('users', GetUsers.as_view()),
]