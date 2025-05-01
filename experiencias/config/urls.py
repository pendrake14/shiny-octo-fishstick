from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

swagger = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/users/', include('users.urls')),
] + swagger