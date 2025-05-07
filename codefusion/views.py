from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Country
from .serializers import CountrySerializer

def index(request):
    # Count total countries in database
    country_count = Country.objects.count()
    return HttpResponse(f'<h1>CodeFusion Country Data</h1><p>{country_count} countries in database.</p>')


class CountryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CountrySerializer
    pagination_class = CountryPagination
    
    def get_queryset(self):
        queryset = Country.objects.all()
        
        # Search by name or capital
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name_common__icontains=search_query) | 
                Q(name_official__icontains=search_query) |
                Q(capital__icontains=search_query)
            )
        
        # Filter by region
        region = self.request.query_params.get('region', None)
        if region:
            queryset = queryset.filter(region__icontains=region)
            
        return queryset.prefetch_related('currencies', 'languages')