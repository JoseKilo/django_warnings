from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Warning
from .serializers import WarningModelSerializer


class WarningViewSet(ReadOnlyModelViewSet):
    """
    A ViewSet for working with Warning objects

    It can be extended to change the Warning fields to be used:

        class MyWarningViewSet(WarningViewSet):
            serializer_fields = ('message', 'last_generated')
    """

    queryset = Warning.objects.all()
    serializer_class = WarningModelSerializer
    serializer_fields = ('id', 'message', 'identifier', 'url_params')
    http_method_names = ('get', 'post')

    def get_serializer(self, *args, **kwargs):
        """
        Override the dafault method to include the `fields` parameter

        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        return serializer_class(
            context=context, fields=self.serializer_fields, *args, **kwargs)

    @detail_route(methods=['post'])
    def acknowledge(self, request, pk=None):
        """
        Acknowledge a given Warning object. Optional `user_id` can be specified
        """
        warning = self.get_object()
        user_id = request.DATA.get('user_id')

        warning.acknowledge(user_id=user_id)

        serializer = self.get_serializer(instance=warning)
        warning_data = serializer.data
        return Response(warning_data)
