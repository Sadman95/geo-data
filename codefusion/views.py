
from django.shortcuts import render
from django.http import HttpResponse
from .models import Country
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CountrySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def index(request):
    # Count total countries in database
    return HttpResponse(f'<h1>Index</h1><div><a href="http://localhost:8000/countries">countries</a></div>')


def country_list_view(request):
    query = request.GET.get('q', '')
    region = request.GET.get('region', '')
    
    countries = Country.objects.all()
    

    if query:
        countries = countries.filter(
            Q(name_common__icontains=query) |
            Q(cca2__icontains=query) |
            Q(capital__icontains=query)
        )
    
    if region:
        countries = countries.filter(region__iexact=region)

    # Get distinct regions for the dropdown
    regions = Country.objects.values_list('region', flat=True).distinct().order_by('region')

    return render(request, 'country_list.html', {
        'countries': countries,
        'query': query,
        'region': region,
        'regions': regions,
    })

def same_region_countries(request):
    country_name = request.GET.get('country')

    if not country_name:
        return JsonResponse({'error': 'Missing country parameter'}, status=400)

    country = get_object_or_404(Country, name_common__iexact=country_name)
    region = country.region

    other_countries = (
        Country.objects
        .filter(region=region)
        .exclude(pk=country.pk)
        .values_list('name_common', flat=True)
    )

    return JsonResponse(list(other_countries), safe=False)

class CountryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    pagination_class = CountryPagination
    
    def get_queryset(self):
        queryset = Country.objects.all().prefetch_related('currencies', 'languages')
        
        # Search by name or capital
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name_common__icontains=search_query) | 
                Q(name_official__icontains=search_query)
            )
        
        # Filter by region
        region = self.request.query_params.get('region', None)
        if region:
            queryset = queryset.filter(region__icontains=region)
            
        # Filter by language name
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(languages__name__iexact=language)
        
        # Sorting
        sort_by = self.request.query_params.get('sort_by', 'id')
        sort_order = self.request.query_params.get('sort_order', 'asc')
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)
            
        return queryset.prefetch_related('currencies', 'languages')
class CountryDetailView(RetrieveAPIView):
    """
    API endpoint that retrieves a single country by ID.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'id'