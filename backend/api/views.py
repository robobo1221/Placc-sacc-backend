from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from rest_framework import serializers
from django.db import models
import math

from achievements.models import Achievement
from user.models import User, UserAchievement

class RegisterAchievementToUser(APIView):
    def post(self, request):
        achievement_code = request.data.get('achievement_code')
        username = request.data.get('username')

        try:
            achievement = Achievement.objects.get(code=achievement_code)
            user = User.objects.get(username=username)
        except (Achievement.DoesNotExist, User.DoesNotExist):
            return Response({'error': 'Invalid achievement code or username'}, status=status.HTTP_400_BAD_REQUEST)

        if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            return Response({'error': 'User already has this achievement'}, status=status.HTTP_400_BAD_REQUEST)
        
        current_datetime = datetime.now()

        # Check if current date and time are within achievement bounds (null-safe)
        if (
            (achievement.start_date and current_datetime.date() < achievement.start_date) if achievement.start_date else False or
            (achievement.end_date and current_datetime.date() > achievement.end_date) if achievement.end_date else False or
            (achievement.start_time and current_datetime.time() < achievement.start_time) if achievement.start_time else False or
            (achievement.end_time and current_datetime.time() > achievement.end_time) if achievement.end_time else False
        ):
            return Response({'error': 'Current date or time is outside achievement bounds'}, status=status.HTTP_400_BAD_REQUEST)

        user_achievement = UserAchievement(user=user, achievement=achievement)
        user_achievement.save()

        return Response({'success': 'Achievement registered successfully'}, status=status.HTTP_201_CREATED)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")

class AchievementSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'code', 'description', 'points', 'category', 'latitude', 'longitude', 'start_date', 'end_date', 'start_time', 'end_time', 'image_url')

    def get_category(self, obj):
        return obj.get_category_display()
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()
    class Meta:
        model = UserAchievement
        fields = ('achievement',)

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', None)
        super(UserAchievementSerializer, self).__init__(*args, **kwargs)

        if context:
            self.fields['achievement'] = AchievementSerializer(context=context)
class GetUserAchievements(APIView):
    def get(self, request):
        username = request.query_params.get("username")

        if not username:
            return Response({'error': 'No username specified'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_achievements = UserAchievement.objects.filter(user__username=username)
        serializer = UserAchievementSerializer(user_achievements, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

def distance(lat1, lon1, lat2, lon2): 
    R = 6371  # Radius of the earth in km 
    dLat = math.radians(lat2 - lat1) 
    dLon = math.radians(lon2 - lon1) 
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2) 
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
    d = R * c  # Distance in km 
    return d

class GetAchievements(APIView):
    def get(self, request):
        username = request.query_params.get("username")
        longitude = request.query_params.get("longitude")
        latitude = request.query_params.get("latitude")
        maxnum = request.query_params.get("max")

        achievements = Achievement.objects.all()

        if username:
            achievements = achievements.exclude(
                userachievement__user__username=username
            )

        if maxnum:
            achievements = achievements[:int(maxnum)]

        if longitude and latitude:
            achievements = sorted(
                achievements,
                key=lambda achievement: distance(
                    float(achievement.latitude), float(achievement.longitude), float(latitude), float(longitude)
                )
            )

        serializer = AchievementSerializer(achievements, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAchievementId(APIView):
    def get(self, request, id):
        achievement = Achievement.objects.filter(pk=id)

        if not achievement:
            return Response({'error': 'No achievement found with this id'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(AchievementSerializer(achievement.get(), context={'request': request}).data, status=status.HTTP_200_OK)
    
class GetAchievementCode(APIView):
    def get(self, request, code):
        achievement = Achievement.objects.filter(code=code)

        if not achievement:
            return Response({'error': 'No achievement found with this code'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(AchievementSerializer(achievement.get(), context={'request': request}).data, status=status.HTTP_200_OK)
    
class GetUser(APIView):
    def get(self, request, username):
        user = User.objects.filter(username=username)

        if not user:
            return Response({'error': 'No user found with thi username'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(UserSerializer(user.first()).data, status=status.HTTP_200_OK)
    
class GetUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)

