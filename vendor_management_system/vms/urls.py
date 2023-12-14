from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vms import views
from vms.views import VendorViewSet, PurchaseOrderViewSet, VendorPerformanceViewSet

urlpatterns = [
    path("", views.index, name="index"),
]



router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendors')
router.register(r'purchase_orders', PurchaseOrderViewSet, basename='purchase_orders')



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/vendors/<str:vendor_code>/', VendorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='vendor-detail'),
    path('api/purchase_orders/', PurchaseOrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='purchaseorder-list'),
    path('api/purchase_orders/<str:po_number>/', PurchaseOrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='purchaseorder-detail'),
    path('api/vendors/<str:pk>/performance/', VendorPerformanceViewSet.as_view({'get': 'retrieve'}), name='vendor_performance'),
    path('api/purchase_orders/<str:po_number>/acknowledge', PurchaseOrderViewSet.as_view({'post': 'acknowledge'}), name='purchase-acknowledge'),
    path('api-token-auth/', views.obtain_auth_token)
]