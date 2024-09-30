"""
URL configuration for cloudserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# cloudserver/urls.py

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from cloudapp import views  # views 모듈을 임포트


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cloudapp/', include('cloudapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django 내장 인증 URL
    path('', views.home, name='home'),  # 루트 URL 패턴 추가
    path('cloudapp/', include('cloudapp.urls')),  # cloudapp 앱의 URL 포함
    path('accounts/', include('allauth.urls')),  # allauth 인증 URL
    path('delete_file/<int:id>/', views.delete_file, name='delete_file'),
    path('', include('django_prometheus.urls')),  # Prometheus 메트릭 URL을 변경
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)