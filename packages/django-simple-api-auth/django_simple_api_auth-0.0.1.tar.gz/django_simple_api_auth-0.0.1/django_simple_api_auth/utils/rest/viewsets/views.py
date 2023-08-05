from rest_framework.viewsets import GenericViewSet


class MultiPermissionsApiViewMixin(GenericViewSet):
    permission_classes_dict = {}

    def get_permissions(self):
        self.permission_classes = self.permission_classes_dict.get(self.action, self.permission_classes)
        return super().get_permissions()


class MultiSerializersApiViewMixin(GenericViewSet):
    serializer_classes_dict = {}

    def get_serializer_class(self):
        self.serializer_class = self.serializer_classes_dict.get(self.action, self.serializer_class)
        return super().get_serializer_class()


class MultiConfApiViewMixin(MultiSerializersApiViewMixin, MultiPermissionsApiViewMixin):
    pass