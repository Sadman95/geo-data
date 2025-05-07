from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'countries', views.CountryViewSet, basename='country')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
]