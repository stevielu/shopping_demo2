from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from goods.serializer import GoodsSerializer
from .models import UserAddress
class UserFavDetailsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods",'id')

class UserFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user','goods'),
                message='该商品已收藏'
            )
        ]
        fields = ("user","goods",'id')

class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserAddress
        fields = "__all__"