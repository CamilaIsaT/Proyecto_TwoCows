from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.rol == 'ADMIN'
    
class IsCuidadorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.rol in ['ADMIN', 'CUIDADOR']
    
class IsOrdenadorForProduccion(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.rol == 'ADMIN':
            return True
        if request.user.rol == 'ORDENADOR':
            if request.method in ['GET', 'POST']:
                return True
            return False