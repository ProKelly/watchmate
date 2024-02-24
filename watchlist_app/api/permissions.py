
from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):#use has_permission method since inheriting from a none abstract class

    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)#checks if the use is an admin

class ReviewUserOrReadOnly(permissions.BasePermission):#use has_object_permission since inheriting from an abstract class

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff#checks if the Object user is the logged in user