from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.permissions import IsAdminUser
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Horeca 360 API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="xoliqberdiyevbehru12@gmail.com"),
      license=openapi.License(name="Felix IT Solutions License"),
   ),
   public=True,
   permission_classes=[IsAdminUser]
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/', include(
      [
         path('accounts/', include('core.apps.accounts.urls')),
         path('orders/', include('core.apps.orders.urls')),
         path('products/', include('core.apps.products.urls')),
         path('shared/', include('core.apps.shared.urls')),
         path('admin/', include('core.apps.admin_panel.urls')),
         path('objects/', include('core.apps.objects.urls')),
      ]
   )),

   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)