from django.shortcuts import get_object_or_404

from rest_framework import generics, status, permissions

from core.apps.admin_panel.serializers.objects import ObjectSerializer
from core.apps.products.models import Object
from core.apps.shared.mixins.response import ResponseMixin


class ObjectCreateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return self.success_response(message='koplik qoshildi', status_code=status.HTTP_201_CREATED)
        return self.failure_response(message='koplik qoshishda xatolik', data=serializer.errors)


class ObjectListApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class ObjectDeleteApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, id):
        object = get_object_or_404(Object, id=id)
        object.delete()
        return self.success_response(message='birlik ochirildi', status_code=status.HTTP_204_NO_CONTENT)


class ObjectUpdateApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, id):
        object = get_object_or_404(Object, id=id)
        serializer = self.serializer_class(data=request.data, instance=object)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(message='koplik tahrirlandi')
        return self.failure_response(message='hatolik', data=serializer.errors)


class ObjectDetailApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = ObjectSerializer
    queryset = Object.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, id):
        object = get_object_or_404(Object, id=id)
        serializer = self.serializer_class(object)
        return self.success_response(message='koplik malumotlari', data=serializer.data)
