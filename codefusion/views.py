
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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm


# views


def index(request):
    # Count total countries in database
    return HttpResponse('<h1>Index</h1><div><a href="http://localhost:8000/countries">countries</a></div>')

@login_required
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
    
    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('country-list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



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