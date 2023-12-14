# vms/models.py

from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True, primary_key=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        db_table = 'vendor'


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, primary_key=True)
    # ForeignKey establishes a link between the PurchaseOrder model and the Vendor model.
    # Here, on_delete=models.CASCADE specifies that if a vendor is deleted, all associated purchase orders will also be deleted
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO Number: {self.po_number}, Vendor: {self.vendor.name}"

    class Meta:
        managed = True
        db_table = 'purchase_order'
        
class HistoricalPerformance(models.Model):
    # ForeignKey establishes a link between the HistoricalPerformance model and the Vendor model.
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - Historical Performance on {self.date}"

    class Meta:
        managed = True
        db_table = 'historical_performance'