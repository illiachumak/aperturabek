from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, FeedbackViewSet


router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register('feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
]