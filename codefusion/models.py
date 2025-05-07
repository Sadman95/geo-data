
from django.db import models

class Country(models.Model):
    # Common name of the country (e.g. "United States")
    name_common = models.CharField(max_length=100)
    # Official name of the country (e.g. "United States of America")
    name_official = models.CharField(max_length=200)
    # Country code (e.g. "US")
    cca2 = models.CharField(max_length=2, unique=True)
    # Three-letter country code (e.g. "USA")
    cca3 = models.CharField(max_length=3, unique=True)
    # Country calling code (e.g. "1" for US)
    calling_code = models.CharField(max_length=20, null=True, blank=True)
    # Capital city
    capital = models.CharField(max_length=100, null=True, blank=True)
    # Region (e.g. "Americas")
    region = models.CharField(max_length=100, null=True, blank=True)
    # Subregion (e.g. "North America")
    subregion = models.CharField(max_length=100, null=True, blank=True)
    # Population
    population = models.BigIntegerField(default=0)
    # Area in square kilometers
    area = models.FloatField(null=True, blank=True)
    # URL to the country flag image
    flag_png = models.URLField(max_length=300, null=True, blank=True)
    # URL to the SVG version of the flag
    flag_svg = models.URLField(max_length=300, null=True, blank=True)
    # Latitude/Longitude coordinates
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    # Is the country landlocked?
    landlocked = models.BooleanField(default=False)
    # UN Member status
    un_member = models.BooleanField(default=False)
    # Independent status
    independent = models.BooleanField(default=True)
    # Raw JSON data (for fields we don't explicitly model)
    raw_data = models.JSONField(null=True, blank=True)
    # When the record was created
    created_at = models.DateTimeField(auto_now_add=True)
    # When the record was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_common

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name_common']


class Currency(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='currencies')
    code = models.CharField(max_length=10)  # e.g. USD
    name = models.CharField(max_length=100)  # e.g. US Dollar
    symbol = models.CharField(max_length=10, null=True, blank=True)  # e.g. $

    def __str__(self):
        return f"{self.code} ({self.country.name_common})"

    class Meta:
        verbose_name_plural = "Currencies"


class Language(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='languages')
    code = models.CharField(max_length=10)  # e.g. eng
    name = models.CharField(max_length=100)  # e.g. English

    def __str__(self):
        return f"{self.name} ({self.country.name_common})"

    class Meta:
        verbose_name_plural = "Languages"


class Border(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='borders')
    neighbor = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='neighboring_countries')

    def __str__(self):
        return f"{self.country.name_common} - {self.neighbor.name_common}"

    class Meta:
        unique_together = ('country', 'neighbor')
