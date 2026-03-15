from django.db import models
from core.models import BaseModel

class VendorProductMapping(BaseModel):
    vendor = models.ForeignKey('vendor.Vendor', on_delete=models.CASCADE, related_name='product_mappings')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='vendor_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vendor', 'product'], name='unique_vendor_product_mapping')
        ]

    def __str__(self):
        return f"{self.vendor.name} - {self.product.name}"
