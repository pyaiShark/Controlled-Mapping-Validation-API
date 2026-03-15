from rest_framework import serializers
from .models import ProductCourseMapping

class ProductCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCourseMapping
        fields = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Assignment Requirement: only one primary_mapping=True for a parent at that level
        product = data.get('product')
        primary_mapping = data.get('primary_mapping', False)

        # Self instance ID to handle updates properly
        instance_id = self.instance.id if self.instance else None

        if primary_mapping and product:
            existing_primary = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if instance_id:
                existing_primary = existing_primary.exclude(id=instance_id)

            if existing_primary.exists():
                raise serializers.ValidationError({
                    "primary_mapping": "This product already has a primary course mapping."
                })

        return data
