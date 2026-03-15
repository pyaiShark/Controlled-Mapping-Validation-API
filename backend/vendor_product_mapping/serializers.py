from rest_framework import serializers
from .models import VendorProductMapping

class VendorProductMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProductMapping
        fields = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Assignment Requirement: only one primary_mapping=True for a parent at that level
        vendor = data.get('vendor')
        primary_mapping = data.get('primary_mapping', False)

        # Self instance ID to handle updates properly
        instance_id = self.instance.id if self.instance else None

        if primary_mapping and vendor:
            existing_primary = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if instance_id:
                existing_primary = existing_primary.exclude(id=instance_id)

            if existing_primary.exists():
                raise serializers.ValidationError({
                    "primary_mapping": "This vendor already has a primary product mapping."
                })

        return data
