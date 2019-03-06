
from rest_framework import serializers
from .models import Goods,GoodsCategory,GoodsImage

class SubCategorySerializerLevel2(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class SubCategorySerializerLevel1(serializers.ModelSerializer):
    sub_cat = SubCategorySerializerLevel2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    sub_cat = SubCategorySerializerLevel1(many = True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = "__all__"

class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = "__all__"