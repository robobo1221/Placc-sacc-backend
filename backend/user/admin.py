from django.contrib import admin
from .models import User, UserAchievement

# Register your models here.

admin.site.register(User)
admin.site.register(UserAchievement)

from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group

admin.site.unregister(DjangoUser)
admin.site.unregister(Group)