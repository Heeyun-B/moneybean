from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'nickname')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            nickname=validated_data['nickname'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'is_staff')

class DepositSubscriptionSerializer(serializers.ModelSerializer):
    """가입한 예금 상품"""
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    bank_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    product_code = serializers.CharField(source='product.fin_prdt_cd', read_only=True)
    interest_rate = serializers.FloatField(source='selected_option.intr_rate', read_only=True)
    save_term = serializers.IntegerField(source='selected_option.save_trm', read_only=True)
    
    class Meta:
        from deposits.models import DepositSubscription
        model = DepositSubscription
        fields = ('id', 'product_code', 'product_name', 'bank_name', 
                  'interest_rate', 'save_term', 'subscribed_at')


class SavingSubscriptionSerializer(serializers.ModelSerializer):
    """가입한 적금 상품"""
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    bank_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    product_code = serializers.CharField(source='product.fin_prdt_cd', read_only=True)
    interest_rate = serializers.FloatField(source='selected_option.intr_rate', read_only=True)
    save_term = serializers.IntegerField(source='selected_option.save_trm', read_only=True)
    
    class Meta:
        from deposits.models import SavingSubscription
        model = SavingSubscription
        fields = ('id', 'product_code', 'product_name', 'bank_name', 
                  'interest_rate', 'save_term', 'subscribed_at')
        
class UserProfileSerializer(serializers.ModelSerializer):
    """프로필 조회용 Serializer"""
    deposit_subscriptions = DepositSubscriptionSerializer(many=True, read_only=True)
    saving_subscriptions = serializers.SerializerMethodField()

    def get_saving_subscriptions(self, obj):
        from deposits.models import SavingSubscription
        subscriptions = SavingSubscription.objects.filter(user=obj)
        return SavingSubscriptionSerializer(subscriptions, many=True).data
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'first_name', 'last_name', 'date_joined', 'deposit_subscriptions', 'saving_subscriptions')
        read_only_fields = ('id', 'username', 'date_joined')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """프로필 수정용 Serializer"""
    class Meta:
        model = User
        fields = ('email', 'nickname', 'first_name', 'last_name')
    
    def validate_nickname(self, value):
        """닉네임 중복 체크 (자기 자신 제외)"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """비밀번호 변경용 Serializer"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 일치하지 않습니다.")
        return value
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "새 비밀번호가 일치하지 않습니다."})
        return data