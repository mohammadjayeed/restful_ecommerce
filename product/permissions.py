from rest_framework import permissions

class IsAdminUserForPost(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user and request.user.is_staff
        return False
    


class IsAdminUserForUpdateDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if request.method == 'GET':
            return True
        
        if request.method in ['PUT', 'DELETE']:
            return request.user and request.user.is_staff
        return False