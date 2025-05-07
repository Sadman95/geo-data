
from django.shortcuts import render
from django.http import HttpResponse
from .models import Country

def index(request):
    # Count total countries in database
    country_count = Country.objects.count()
    return HttpResponse(f'<h1>CodeFusion Country Data</h1><p>{country_count} countries in database.</p>')
