from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [

    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-ui'),
    path('download/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
