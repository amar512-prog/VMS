from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F, Sum
from django.utils import timezone
from vms.models import Vendor, PurchaseOrder, HistoricalPerformance
from vms.serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
import pytz
from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
def obtain_auth_token(request):
    username = 'admin'
    password = 'admin'
    user = None
    if not User.objects.filter(username=username).exists():
        # Create a new user
        user = User.objects.create_user(username=username, password=password)
    else:
        user = User.objects.get(username=username)
    token = Token.objects.create(user=user)
    print(f"Token:{token.key}")
    return { 'token' : token.key}
def index(request):
    return HttpResponse("Hello, world!!!")


# class VendorViewSet(viewsets.ModelViewSet):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer
    

class VendorViewSet(viewsets.ViewSet):
    def create(self, request):
        #print(request, request.data)
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #print(serializer, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def list(self, request):
        queryset = Vendor.objects.all()
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        #print(request, pk)
        try:
            vendor = Vendor.objects.get(vendor_code=pk)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(vendor_code=pk)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(vendor_code=pk)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        vendor.delete()
        return Response({"success": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class PurchaseOrderViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        vendor_id = request.query_params.get('vendor')  # Get the vendor ID from query parameters if provided
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def acknowledge(self, request, po_number=None):
        #try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
        if purchase_order.status == 'pending':
            current_time =  timezone.localtime(timezone.now()+timezone.timedelta(hours=5,minutes=30)) 
            # Update acknowledgment_date
            purchase_order.acknowledgment_date = current_time
            purchase_order.save()
            
            return Response({"message": "Purchase Order acknowledged successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Cannot acknowledge a completed or canceled order"}, status=status.HTTP_400_BAD_REQUEST)
        # except PurchaseOrder.DoesNotExist:
        #     return Response({"message": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)
        


@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    #current_time = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
    current_time = timezone.localtime(timezone.now()+timezone.timedelta(hours=5,minutes=30)) 
    if instance.status == 'completed':
        vendor_id = instance.vendor
        print("instance:",instance, sender, created, instance.acknowledgment_date)
        vendor_orders = PurchaseOrder.objects.filter(vendor=vendor_id, status='completed')
        total_completed_orders = vendor_orders.count()
        print(vendor_orders, total_completed_orders, vendor_orders)
        # Filter completed orders that were delivered on or before the delivery date
        on_time_delivered_orders = vendor_orders.filter(acknowledgment_date__lte=F('delivery_date'))
        print("on time:", on_time_delivered_orders)
        total_on_time_delivered = on_time_delivered_orders.count()

        if total_completed_orders > 0:
            on_time_delivery_rate = (total_on_time_delivered / total_completed_orders) * 100.0
        else:
            on_time_delivery_rate = 0.0
        print("rate", on_time_delivery_rate)
        # Update or create HistoricalPerformance entry for the vendor
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor_id,
            defaults={
                'date':current_time,
                'on_time_delivery_rate': 0.0, 
                'quality_rating_avg': 0.0,
                'average_response_time': 0.0,
                'fulfillment_rate': 0.0
            })
        historical_performance.date = current_time
        historical_performance.on_time_delivery_rate = on_time_delivery_rate
        # Populate other fields like date, quality_rating_avg, etc. as needed
        historical_performance.save()
        
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor_id = instance.vendor

        # Filter completed orders with quality rating for the vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor_id, status='completed', quality_rating__isnull=False)
        total_completed_orders = completed_orders.count()

        # Calculate the average quality rating for completed orders
        total_quality_rating = completed_orders.aggregate(total_rating=Sum('quality_rating'))['total_rating']
        quality_rating_avg = total_quality_rating / total_completed_orders if total_completed_orders > 0 else 0.0

        # Update or create HistoricalPerformance entry for the vendor
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor_id,
            defaults={
                'date':current_time,
                'on_time_delivery_rate': 0.0, 
                'quality_rating_avg': 0.0,
                'average_response_time': 0.0,
                'fulfillment_rate': 0.0
            })
        historical_performance.date = current_time
        historical_performance.quality_rating_avg = quality_rating_avg
        # Update other fields if needed
        historical_performance.save()
        
    if instance.acknowledgment_date is not None:
        vendor_id = instance.vendor

        # Fetch all completed orders for the vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor_id, acknowledgment_date__isnull=False)

        # Calculate response time for each order and get the sum of all response times
        total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() for order in completed_orders)

        # Calculate the average response time
        average_response_time = total_response_time / completed_orders.count() if completed_orders.count() > 0 else 0.0
        
        # Update or create HistoricalPerformance entry for the vendor
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor_id,
            defaults={
                'date':current_time,
                'on_time_delivery_rate': 0.0, 
                'quality_rating_avg': 0.0,
                'average_response_time': 0.0,
                'fulfillment_rate': 0.0
            })
        historical_performance.date = current_time
        historical_performance.average_response_time = average_response_time
        # Update other fields if needed
        historical_performance.save()
        
    vendor_id = instance.vendor

    # Fetch all orders for the vendor
    all_orders = PurchaseOrder.objects.filter(vendor=vendor_id)

    # Count completed orders without issues
    completed_orders_without_issues = all_orders.filter(status='completed', issue_date__isnull=False)

    total_orders = all_orders.count()
    total_completed_without_issues = completed_orders_without_issues.count()

    # Calculate fulfilment rate
    fulfilment_rate = (total_completed_without_issues / total_orders) * 100 if total_orders > 0 else 0.0
       
    # Update or create HistoricalPerformance entry for the vendor
    historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor_id,
        defaults={
            'date':current_time,
            'on_time_delivery_rate': 0.0, 
            'quality_rating_avg': 0.0,
            'average_response_time': 0.0,
            'fulfillment_rate': 0.0
        })
    historical_performance.date = current_time
    historical_performance.fulfillment_rate = fulfilment_rate
    # Update other fields if needed
    historical_performance.save()
    
class VendorPerformanceViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            historical_performance = HistoricalPerformance.objects.get(vendor=pk)
            print(historical_performance)
            serializer = VendorPerformanceSerializer(historical_performance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (Vendor.DoesNotExist, HistoricalPerformance.DoesNotExist):
            return Response({"message": "Vendor performance metrics not found"}, status=status.HTTP_404_NOT_FOUND)
    