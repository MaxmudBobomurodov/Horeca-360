from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions

from core.apps.admin_panel.serializers.objects import ObjectSerializer
from core.apps.products.models import Object
from core.apps.shared.mixins.response import ResponseMixin


# Create your views here.
class ObjectListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="List all objects",
        responses={200: ObjectSerializer(many=True)}
    )

    def get(self, request):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)