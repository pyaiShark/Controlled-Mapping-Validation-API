from django.db import models
from core.models import BaseModel

class CourseCertificationMapping(BaseModel):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='certification_mappings')
    certification = models.ForeignKey('certification.Certification', on_delete=models.CASCADE, related_name='course_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'certification'], name='unique_course_certification_mapping')
        ]

    def __str__(self):
        return f"{self.course.name} - {self.certification.name}"
