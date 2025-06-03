from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from rest_framework import routers
from decor import settings
from item.views import ItemViewSet, CategoryViewSet, SubCategoryViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


router = routers.DefaultRouter()

router.register('items', ItemViewSet)
router.register('categories', CategoryViewSet)
router.register('sub-categories', SubCategoryViewSet)
# router.register('auth', )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('item.urls')),
    path('', include('authentication.urls')),
    path('schema/', include('decor.schema_urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]
