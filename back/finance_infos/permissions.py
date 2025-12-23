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
        return request.user and request.user.is_staff