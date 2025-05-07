from rest_framework import serializers
from .models import Country, Currency, Language

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code', 'name']


class CountrySerializer(serializers.ModelSerializer):
    currencies = CurrencySerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Country
        fields = [
            'id', 'name_common', 'name_official', 'cca2', 'cca3', 
            'capital', 'region', 'subregion', 'population', 'area',
            'flag_png', 'flag_svg', 'lat', 'lng', 'landlocked',
            'currencies', 'languages'
        ]