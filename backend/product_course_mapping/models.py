from django.db import models
from core.models import BaseModel

class ProductCourseMapping(BaseModel):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='course_mappings')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='product_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'course'], name='unique_product_course_mapping')
        ]

    def __str__(self):
        return f"{self.product.name} - {self.course.name}"
