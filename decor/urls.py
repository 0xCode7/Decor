from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers
from decor import settings
from item.views import ItemViewSet, CategoryViewSet, SubCategoryViewSet

router = routers.DefaultRouter()

router.register('items', ItemViewSet)
router.register('categories', CategoryViewSet)
router.register('sub-categories', SubCategoryViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)