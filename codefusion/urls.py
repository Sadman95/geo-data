from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'countries', views.CountryViewSet, basename='country')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/countries/<int:pk>/', views.CountryDetailView.as_view(), name='country-detail'),
]