from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializer import ShoppingCartSerializer,OrderSerializer,ShoppingCartDetailsSerializer,OrderSerializerDetails
from .models import ShoppingCart, OrderInfo,OrderGoods
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.

class ShoppingCartViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailsSerializer
        else:
            return ShoppingCartSerializer

class OrderViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    订单管理
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderSerializerDetails
        else:
            return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_cart_goods = ShoppingCart.objects.filter(user=self.request.user)
        for goods_in_cart in shop_cart_goods:
            order_goods = OrderGoods()
            order_goods.goods = goods_in_cart.goods
            order_goods.goods_num = goods_in_cart.goods_num
            order_goods.order = order
            order_goods.save()

            shop_cart_goods.delete()
        return order

