from django.contrib import admin
from address.models import City, District


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'scope_uuid')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
