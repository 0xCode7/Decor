from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from rest_framework import routers
from decor import settings
from item.views import ItemViewSet, CategoryViewSet, SubCategoryViewSet, BestSellerAPIView, SliderAPIView

router = routers.DefaultRouter()

router.register('items', ItemViewSet)
router.register('categories', CategoryViewSet)
router.register('sub-categories', SubCategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('best-seller/', BestSellerAPIView.as_view(), name='best-seller-list'),
    path('slider/', SliderAPIView.as_view(), name='slider-list'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]
