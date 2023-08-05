class DenyAny:
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class PostWithoutAuth:
    def has_permission(self, request, view):
        return request.method == "POST"
