from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import OrderProduct, Order, Feedback
from rest_framework import status
from .serializers import OrderSerializer, FeedbackSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
import random


# Create your views here.

class CustomPaginator(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

def is_admin(user):
    return user.is_superuser

class OrderViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPaginator
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
        

    def retrieve(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, id = pk)
        order = OrderSerializer(order)
        return Response(order.data)
    

    def create(self, request, *args, **kwargs):
        data = request.data
        new_order = Order.objects.create(name=data['name'], number=data['phone'], email=data['email'], total_price = 0)
        products = data["products"]
        price = 0
        
        for product in products:
            OrderProduct.objects.create(product_name = product['title'],
                                                    image = product['image'].split('?')[0],
                                                    color = product['color'],
                                                    price = float(product['total_price']),
                                                    modifications = product['options'],
                                                    quantity = product['quantity'],
                                                    orderId = new_order
                                                    )
            price += product['quantity']*float(product['total_price'])

        print = price
        new_order.total_price = price
        new_order.save()

        new_order.order_number = str(random.randint(10000, 999999) + new_order.id)

        resp = OrderSerializer(new_order).data
        return Response(resp)
    
    def update(self, request, pk, *args, **kwargs):
        data = request.data
        order = get_object_or_404(Order, id=pk)
        order.status = data.get('status', order.status)
        order.payment = data.get('payment', order.payment)
        order.save()
        resp = OrderSerializer(order).data
        return Response(resp)

    def list(self, request):
        pend = OrderSerializer(Order.objects.filter(status = Order.PENDING).order_by('-date_created'), many=True).data
        work = OrderSerializer(Order.objects.filter(status = Order.WORKING).order_by('-date_created'), many=True).data
        done = OrderSerializer(Order.objects.filter(status = Order.DONE).order_by('-date_created'), many=True).Data
        context = {'PENDING': pend, 'WORKING': work, 'DONE': done}
        return Response(context)
    
    
    

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    
    def get_permissions(self):
        if self.action == 'create' :
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
        
    def retrieve(self, request, pk, *args, **kwargs):
       order = get_object_or_404(Feedback, id = pk)
       order = FeedbackSerializer(order)
       return Response(order.data)
               
    def create(self, request, *args, **kwargs):
        data = request.data
        new_feedback = Feedback.objects.create(name = data['name'], number = data['number'])
        return Response(FeedbackSerializer(new_feedback).data)
    
    def update(self, request, pk, *args, **kwargs):
        data = request.data
        feedback = get_object_or_404(Feedback, id=pk)
        feedback.is_Called = data['is_Called']
        feedback.save()
        return Response(FeedbackSerializer(feedback).data)

    def list(self, request):
        ready = FeedbackSerializer(Feedback.objects.filter(is_Called = True), many=True).data
        notready = FeedbackSerializer(Feedback.objects.filter(is_Called = False), many=True).data
        context = {'PENDING': notready, 'DONE':ready,}
        return Response(context)
