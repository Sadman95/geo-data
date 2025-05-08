from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view


# routers

router = DefaultRouter(trailing_slash=False)
router.register(r'countries', views.CountryViewSet, basename='country')

urlpatterns = [
    path('', views.index, name='index'),
    path('api', include(router.urls)),
    path('api/countries/<int:pk>', views.CountryDetailView.as_view(), name='country-detail'),
    path('register', register_view, name='register'),
     path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('countries', views.country_list_view, name='country-list'),
]