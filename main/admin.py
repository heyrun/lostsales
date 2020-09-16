from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Products)
admin.site.register(Staff)


admin.site.register(Region)


@admin.register(Lostsales)
class ProductResources(ImportExportModelAdmin):
    readonly_fields = ('created_date',)


@admin.register(Stores)
class ProductResources(ImportExportModelAdmin):
    pass


@admin.register(Products)
class ProductResources(ImportExportModelAdmin):
    readonly_fields = ('id',)
