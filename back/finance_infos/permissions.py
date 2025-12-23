from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    관리자만 작성/수정/삭제 가능, 일반 사용자는 읽기만 가능
    """
    def has_permission(self, request, view):
        # 읽기 권한(GET, HEAD, OPTIONS)은 모두에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 작성/수정/삭제는 관리자만
        # 디버깅용 로그
        print(f"[권한 체크] User: {request.user}, is_authenticated: {request.user.is_authenticated}, is_staff: {request.user.is_staff}")

        # 임시: 개발 환경에서 모든 인증된 사용자 허용 (TODO: 프로덕션 전 제거)
        if request.user and request.user.is_authenticated:
            return True

        return request.user and request.user.is_authenticated and request.user.is_staff