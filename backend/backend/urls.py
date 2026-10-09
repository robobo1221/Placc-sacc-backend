"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
]

# Achievement images and QR codes are uploaded at runtime into static/images/ (see achievements/models.py).
# WhiteNoise only serves files that existed when the server started, so serve these uploads directly.
urlpatterns += [
    re_path(r'^static/images/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / settings.IMAGES_DIR}),
]
