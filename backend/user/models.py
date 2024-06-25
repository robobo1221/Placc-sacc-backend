from django.db import models
from django.core.validators import EmailValidator
from achievements.models import Achievement

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=False, blank=False, validators=[EmailValidator])

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

class UserAchievement(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, verbose_name="Achievement", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.achievement.name}"
    
    class Meta:
        unique_together = ('user', 'achievement')