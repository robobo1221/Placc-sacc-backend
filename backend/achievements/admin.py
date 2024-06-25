from django.contrib import admin
from .models import Achievement

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'category', 'latitude', 'longitude', 'created_at', 'updated_at')
    search_fields = ['name']
    readonly_fields = ['code', 'qrcode']

admin.site.register(Achievement, AchievementAdmin)