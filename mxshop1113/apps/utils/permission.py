from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


        #判断当前传递过来的收藏对象的用户是否是请求用户
        return obj.users == request.user