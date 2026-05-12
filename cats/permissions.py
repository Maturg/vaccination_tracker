from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешение: только владелец может изменять своего кота"""
    
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменение/удаление только владельцу
        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение: только администратор может изменять справочник вакцин"""
    
    def has_permission(self, request, view):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменение только администратору
        return request.user and request.user.is_staff


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для вакцинаций: владелец кота или администратор"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Владелец кота или администратор
        return obj.cat.owner == request.user or request.user.is_staff