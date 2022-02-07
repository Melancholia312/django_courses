from django.http import Http404


class CustomBasePermission:

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class AuthorPermissionMixin(CustomBasePermission):

    def has_permissions(self):
        try:
            return self.get_object().author == self.request.user
        except AttributeError:
            return self.get_object().user == self.request.user
