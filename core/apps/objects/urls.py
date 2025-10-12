from django.urls import path
from core.apps.admin_panel.views import objects as objects_views

urlpatterns = [
path('obyekt/list/', objects_views.ObjectListApiView.as_view()),
]