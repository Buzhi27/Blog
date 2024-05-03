from rest_framework import permissions


# 限制用户权限
class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    仅管理员用户可以修改
    其他用户仅可查看
    """
    # has_permission 方法用于确定用户是否具有执行操作的权限
    def has_permission(self, request, view):
        # SAFE_METHODS 是一个包含只读请求方法（例如 GET、HEAD、OPTIONS）的元组
        # 对所有人允许 GET, HEAD, OPTION 请求
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 仅管理员可进行其他操作
        return request.user.is_superuser
    
