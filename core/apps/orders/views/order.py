from rest_framework import generics, permissions
from rest_framework.response import Response

from core.apps.orders.models import Order, OrderItem, Object
from core.apps.orders.serializers import order as serializers
from core.apps.orders.serializers.order import ObjectSerializer


class OrderCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': 'Firdavs aka order create qilindi, tekshirib koring'},
                status=200
            )
        return Response(
            {
                'success': False,
                "message": "Firdavs aka order create qilishda xatolik chiqdi, errorni oqib koring",
                'error': serializer.errors,
            },
            status=400
        )
    

class OrderListApiView(generics.GenericAPIView):
    serializer_class = serializers.OrderListSerializer
    queryset = Order.objects.prefetch_related('items__product')
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=200)

class ObjectCreateApiView(generics.CreateAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    permission_classes = [permissions.IsAdminUser]

class ObjectListApiView(generics.ListAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    permission_classes = [permissions.IsAuthenticated]
