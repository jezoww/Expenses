from rest_framework.permissions import BasePermission


class ExpenseOwnedPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user != request.user:
          return False
        return True
