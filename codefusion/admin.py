
from django.contrib import admin
from .models import Country, Currency, Language, Border

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name_common', 'cca3', 'capital', 'region', 'population')
    list_filter = ('region', 'subregion', 'landlocked', 'un_member')
    search_fields = ('name_common', 'name_official', 'cca2', 'cca3', 'capital')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name_common', 'name_official', 'cca2', 'cca3', 'capital')
        }),
        ('Geography', {
            'fields': ('region', 'subregion', 'area', 'lat', 'lng', 'landlocked')
        }),
        ('Demographics', {
            'fields': ('population', 'un_member', 'independent')
        }),
        ('Visual', {
            'fields': ('flag_png', 'flag_svg')
        }),
        ('Extra Data', {
            'fields': ('raw_data', 'calling_code', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'country')
    list_filter = ('country__region',)
    search_fields = ('code', 'name', 'country__name_common')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country')
    list_filter = ('country__region',)
    search_fields = ('name', 'code', 'country__name_common')


@admin.register(Border)
class BorderAdmin(admin.ModelAdmin):
    list_display = ('country', 'neighbor')
    list_filter = ('country__region',)
    search_fields = ('country__name_common', 'neighbor__name_common')
