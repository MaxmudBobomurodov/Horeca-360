from django.db.models import Sum
from django.utils import timezone

from rest_framework import generics, views
from rest_framework.permissions import IsAdminUser

from core.apps.orders.models import Order
from core.apps.accounts.models import User
from core.apps.admin_panel.serializers.user import UserSerializer
from core.apps.products.models import Product, Category
from core.apps.shared.mixins.response import ResponseMixin


class DashboardApiView(views.APIView, ResponseMixin):
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = Product.objects.count()
        users = User.objects.count()
        orders = Order.objects.count()
        total_price = (
            Order.objects.filter(created_at__month=timezone.now().month).aggregate(total_price=Sum('total_price'))
        )
        categories = Category.objects.count()
        return self.success_response(
            data={
                'products': products,
                'users': users,
                'orders': orders,
                'categories': categories
            },
            message='dashboard uchun malumotlar statistikasi'
        )
    

class RecentActivityApiView(generics.GenericAPIView, ResponseMixin):
    serializer_class = UserSerializer
    queryset = User.objects.order_by('last_login')
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = self.queryset[:6]
        serializer = self.serializer_class(users, many=True)
        return self.success_response(
            data=serializer.data,
            message='oxirgi kirishlar'
        )

