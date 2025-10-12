from django.urls import path
from core.apps.objects.views import ObjectListApiView

app_name = 'objects'

urlpatterns = [
path('obyekt/list/', ObjectListApiView.as_view()),
]