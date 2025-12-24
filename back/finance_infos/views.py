from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import status
from .models import ArticleInfo, CommentInfo
from .serializers import ArticleInfoSerializer, ArticleInfoListSerializer, CommentInfoSeriallizer
from .permissions import IsAdminOrReadOnly

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # 임시: 개발 중 모든 사용자 허용 (TODO: IsAdminOrReadOnly로 변경)
def info_list(request):
    if request.method == 'GET':
        articles = ArticleInfo.objects.all().order_by('-created_at')
        serializer = ArticleInfoListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 디버깅용 로그
        print(f"[POST 요청] user={request.user}, is_authenticated={request.user.is_authenticated}, is_staff={getattr(request.user, 'is_staff', False)}")

        # 임시: 인증되지 않은 사용자는 거부
        if not request.user.is_authenticated:
            return Response({'error': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ArticleInfoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    
@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAdminOrReadOnly])
def info_detail(request, info_pk):
    try:
        article = ArticleInfo.objects.get(pk=info_pk)
    except ArticleInfo.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ArticleInfoSerializer(article, context={'request': request})
        return Response(serializer.data)
    
    if request.method in ['DELETE', 'PUT']:
        if not request.user.is_staff:
            return Response({'error': '권한이 없습니다.'}, 
                           status=status.HTTP_403_FORBIDDEN)
        
    if request.user != article.user:
        return Response({'error': '권한이 없습니다.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'DELETE':
        article.delete()
        return Response({'message': '게시글이 삭제되었습니다.'}, 
                       status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleInfoSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

            
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, info_pk):
    try:
        article = ArticleInfo.objects.get(pk=info_pk)
    except ArticleInfo.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'},
                       status=status.HTTP_404_NOT_FOUND)

    serializer = CommentInfoSeriallizer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    try:
        comment = CommentInfo.objects.get(pk=comment_pk)
    except CommentInfo.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없습니다.'},
                       status=status.HTTP_404_NOT_FOUND)

    # 작성자만 삭제 가능
    if request.user != comment.user:
        return Response({'error': '권한이 없습니다.'},
                       status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'},
                   status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, info_pk):
    try:
        article = ArticleInfo.objects.get(pk=info_pk)
    except ArticleInfo.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'},
                       status=status.HTTP_404_NOT_FOUND)

    # 이미 좋아요를 눌렀으면 취소, 안 눌렀으면 추가
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
        return Response({'message': '좋아요가 취소되었습니다.', 'is_liked': False},
                       status=status.HTTP_200_OK)
    else:
        article.like_users.add(request.user)
        return Response({'message': '좋아요를 눌렀습니다.', 'is_liked': True},
                       status=status.HTTP_200_OK)