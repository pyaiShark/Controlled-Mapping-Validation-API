from django.contrib import admin
from .models import ProductCourseMapping

@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ('product', 'course', 'primary_mapping', 'is_active')
    list_filter = ('primary_mapping', 'is_active', 'product')
    search_fields = ('product__name', 'course__name')
