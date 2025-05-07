
import json
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from codefusion.models import Country, Currency, Language, Border


class Command(BaseCommand):
    help = 'Fetch country data from restcountries.com API and store in database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing country data...'))
            Country.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared!'))

        self.stdout.write('Fetching countries from API...')
        response = requests.get('https://restcountries.com/v3.1/all')
        
        if response.status_code != 200:
            self.stderr.write(self.style.ERROR(f'API request failed with status code {response.status_code}'))
            return
        
        countries_data = response.json()
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched data for {len(countries_data)} countries'))
        
        # First pass: Create all country records
        with transaction.atomic():
            self.create_country_records(countries_data)
        
        # Second pass: Create relationships (borders, etc.)
        with transaction.atomic():
            self.create_relationships(countries_data)
            
        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))
        
    def create_country_records(self, countries_data):
        self.stdout.write('Creating country records...')
        count = 0
        
        for data in countries_data:
            try:
                # Extract base country data
                name_common = data.get('name', {}).get('common', '')
                name_official = data.get('name', {}).get('official', '')
                cca2 = data.get('cca2', '')
                cca3 = data.get('cca3', '')
                
                # Skip if we don't have the basic identifiers
                if not (name_common and cca2 and cca3):
                    continue
                
                # Get or create the country
                country, created = Country.objects.update_or_create(
                    cca3=cca3,
                    defaults={
                        'name_common': name_common,
                        'name_official': name_official,
                        'cca2': cca2,
                        'capital': data.get('capital', [''])[0] if data.get('capital') else None,
                        'region': data.get('region', ''),
                        'subregion': data.get('subregion', ''),
                        'population': data.get('population', 0),
                        'area': data.get('area'),
                        'flag_png': data.get('flags', {}).get('png'),
                        'flag_svg': data.get('flags', {}).get('svg'),
                        'lat': data.get('latlng', [None, None])[0],
                        'lng': data.get('latlng', [None, None])[1],
                        'landlocked': data.get('landlocked', False),
                        'un_member': data.get('unMember', False),
                        'independent': data.get('independent', True),
                        'calling_code': next(iter(data.get('idd', {}).get('suffixes', [])), '') if data.get('idd', {}).get('root') else None,
                        'raw_data': data
                    }
                )
                
                # Process currencies
                if created:
                    self.create_currencies(country, data.get('currencies', {}))
                    
                    # Process languages
                    self.create_languages(country, data.get('languages', {}))
                
                count += 1
                if count % 50 == 0:
                    self.stdout.write(f'Processed {count} countries')
                    
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error processing country {data.get("name", {}).get("common", "unknown")}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Created/updated {count} country records'))
    
    def create_currencies(self, country, currencies_data):
        for code, details in currencies_data.items():
            Currency.objects.create(
                country=country,
                code=code,
                name=details.get('name', ''),
                symbol=details.get('symbol', '')
            )
    
    def create_languages(self, country, languages_data):
        for code, name in languages_data.items():
            Language.objects.create(
                country=country,
                code=code,
                name=name
            )
    
    def create_relationships(self, countries_data):
        self.stdout.write('Creating border relationships...')
        count = 0
        
        for data in countries_data:
            try:
                country_code = data.get('cca3')
                border_codes = data.get('borders', [])
                
                if not country_code or not border_codes:
                    continue
                
                try:
                    country = Country.objects.get(cca3=country_code)
                    
                    # Add border relationships
                    for border_code in border_codes:
                        try:
                            neighbor = Country.objects.get(cca3=border_code)
                            Border.objects.get_or_create(country=country, neighbor=neighbor)
                            count += 1
                        except Country.DoesNotExist:
                            self.stderr.write(self.style.WARNING(f'Border country {border_code} not found'))
                
                except Country.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f'Country {country_code} not found'))
            
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error processing borders: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} border relationships'))
