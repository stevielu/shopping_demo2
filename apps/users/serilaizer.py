from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta

from .models import VerifyCode


User = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    用户详情
    """
    class Meta:
        model = User
        fields = ("name","gender","mobile","email")

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册
    """
    code = serializers.CharField(required=True, max_length=4,min_length=4,write_only=True,
                                 error_messages={
                                     "blank":"请输入验证码",
                                     "required":"请输入验证码",
                                     "max_length":"格式错误",
                                     "min_length":"格式错误"
                                 },
                                 label="验证码")
    username = serializers.CharField(required=True,allow_blank=False,validators=[UniqueValidator(queryset=User.objects.all(),message="用户已存在")])
    password = serializers.CharField(style={"input_type":'password'},label="密码",write_only= True,)

    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time.replace(tzinfo=None):
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    # def create(self, validated_data):
    #     user = super(UserRegisterSerializer,self).create(validated_data = validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    class Meta:
        model = User
        fields = ("username","code","mobile","password")
