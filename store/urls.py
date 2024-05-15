from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('ok/', view=views.return_ok)
]
