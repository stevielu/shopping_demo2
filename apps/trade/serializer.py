import time
from random import Random
from rest_framework import serializers
from goods.models import Goods
from goods.serializer import GoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods

class ShoppingCartDetailsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = ("goods_num","goods")

class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    goods_num = serializers.IntegerField(required=True, min_value=1, error_messages={
        "min_value":"商品数量小于1",
        "required":"请选择购买数量"
    })

    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True)

    def create(self, validated_data):
        user = self.context["request"].user
        goods_num = validated_data["goods_num"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user,goods=goods)

        if existed:
            existed = existed[0]
            existed.goods_num += goods_num
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.goods_num = validated_data["goods_num"]
        instance.save()
        return instance

class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderSerializerDetails(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    ship_no = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        randdom_ins = Random()
        order_sn = "{time_st}{userid}{randstr}".format(time_st=time.strftime("%Y%m%d%H%M%S"), userid=self.context["request"].user.id, randstr=randdom_ins.randint(1,99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"