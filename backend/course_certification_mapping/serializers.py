from rest_framework import serializers
from .models import CourseCertificationMapping

class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificationMapping
        fields = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Assignment Requirement: only one primary_mapping=True for a parent at that level
        course = data.get('course')
        primary_mapping = data.get('primary_mapping', False)

        # Self instance ID to handle updates properly
        instance_id = self.instance.id if self.instance else None

        if primary_mapping and course:
            existing_primary = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if instance_id:
                existing_primary = existing_primary.exclude(id=instance_id)

            if existing_primary.exists():
                raise serializers.ValidationError({
                    "primary_mapping": "This course already has a primary certification mapping."
                })

        return data
