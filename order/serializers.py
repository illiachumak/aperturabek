from rest_framework import serializers
from .models import *
from django.db.models import Q
from store.models import Modifications


class ModSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()
    class Meta:
        model = Modifications
        fields = ['type', 'name']

class OrderProductSerializer(serializers.ModelSerializer):
    modifications = serializers.SerializerMethodField()

    def get_modifications(self, obj):
        return ModSerializer(Modifications.objects.filter(id__in=obj.modifications), many=True).data

    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        return OrderProductSerializer(OrderProduct.objects.filter(orderId = obj), many=True).data

    class Meta:
        model = Order
        fields = ['id','order_number', 'name', 'number', 'email', 'total_price', 'payment', 'status', 'date_created', 'products']


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'number', 'is_Called']


   
