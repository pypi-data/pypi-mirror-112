from django.http import HttpRequest


class BasePermission:
    def has_permission(self, request: HttpRequest) -> bool:
        return True


class AllowAny(BasePermission):
    def has_permission(self, request: HttpRequest) -> bool:
        return True


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request: HttpRequest) -> bool:
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request: HttpRequest) -> bool:
        return bool(request.user and getattr(request.user, "is_staff", False))


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request: HttpRequest) -> bool:
        return bool(
            request.method in self.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )
