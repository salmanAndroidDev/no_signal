from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """
        Permission class to only access enrolled students
    """

    def has_object_permission(self, request, view, obj):
        """check whether user has enrolled"""
        return obj.students.filter(id=request.user.id).exists()
