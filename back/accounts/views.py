from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """회원가입"""
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # 회원가입 시 자동으로 토큰 생성
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """로그인"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # 사용자 인증
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 토큰 생성 또는 가져오기
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': '로그인 성공',
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': '아이디 또는 비밀번호가 올바르지 않습니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """로그아웃"""
    try:
        # 현재 사용자의 토큰 삭제
        request.user.auth_token.delete()
        return Response({
            'message': '로그아웃되었습니다.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """현재 로그인한 사용자 정보"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_id(request, username):
    """아이디 중복 확인"""
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        return Response({'is_exist': True}, status=status.HTTP_200_OK)
    return Response({'is_exist': False}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request, nickname):
    """닉네임 중복 확인"""
    User = get_user_model()
    if User.objects.filter(nickname=nickname).exists():
        return Response({'is_exist': True}, status=status.HTTP_200_OK)
    return Response({'is_exist': False}, status=status.HTTP_200_OK)