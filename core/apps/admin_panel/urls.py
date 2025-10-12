from django.urls import path, include

from core.apps.admin_panel.views import user as user_views
from core.apps.admin_panel.views import banner as banner_views
from core.apps.admin_panel.views import unity as unity_views
from core.apps.admin_panel.views import category as category_views
from core.apps.admin_panel.views import product as product_views
from core.apps.admin_panel.views import order as order_views
from core.apps.admin_panel.views import dashboard as dashboard_views
from core.apps.admin_panel.views import objects as objects_views

urlpatterns = [
    path('user/', include(
        [
            path('create/', user_views.UserCreateApiView.as_view()),
            path('list/', user_views.UserListApiView.as_view()),
            path('<uuid:id>/update/', user_views.UserUpdateApiView.as_view()),
            path('<uuid:id>/delete/', user_views.UserDeleteApiView.as_view()),
            path('<uuid:id>/', user_views.UserDetailApiView.as_view()),
            path('dashboard/', user_views.UserDashboardApiView.as_view()),
            path('login/', user_views.UserLoginApiView.as_view()),
        ]
    )), 
    path('banner/', include(
        [
            path('create/', banner_views.BannerCreateApiView.as_view()),
            path('list/', banner_views.BannerListApiView.as_view()),
            path('<uuid:id>/', banner_views.BannerDetailApiView.as_view()),
            path('<uuid:id>/update/', banner_views.BannerUpdateApiView.as_view()),
            path('<uuid:id>/delete/', banner_views.BannerDeleteApiView.as_view()),
        ]
    )),
    path('unity/', include(
        [
            path('create/', unity_views.UnityCreateApiView.as_view()),
            path('list/', unity_views.UnityListApiView.as_view()),
            path('<uuid:id>/', unity_views.UnityDetailApiView.as_view()),
            path('<uuid:id>/update/', unity_views.UnityUpdateApiView.as_view()),
            path('<uuid:id>/delete/', unity_views.UnityDeleteApiView.as_view()),
        ]
    )),
    path('obyekt/', include(
        [
            path('create/', objects_views.ObjectCreateApiView.as_view()),
            path('list/', objects_views.ObjectListApiView.as_view()),
            path('<uuid:id>/', objects_views.ObjectDetailApiView.as_view()),
            path('<uuid:id>/update/', objects_views.ObjectUpdateApiView.as_view()),
            path('<uuid:id>/delete/', objects_views.ObjectDeleteApiView.as_view()),
        ]
    )),
    path('category/', include(
        [
            path('create/', category_views.CategoryCreateApiView.as_view()),
            path('list/', category_views.CategoryListApiView.as_view()),
            path('<uuid:id>/update/', category_views.CategoryUpdateApiView.as_view()),
            path('<uuid:id>/delete/', category_views.CategoryDeleteApiView.as_view()),
        ]
    )),
    path('product/', include(
        [
            path('create/', product_views.ProductCreateApiView.as_view()),
            path('list/', product_views.ProductListApiView.as_view()),
            path('<uuid:id>/update/', product_views.ProductUpdateApiView.as_view()),
            path('<uuid:id>/delete/', product_views.ProductDeleteApiView.as_view()),
            path('<uuid:id>/', product_views.ProductDetailApiView.as_view()),
        ]
    )),
    path('order/', include(
        [
            path('list/', order_views.OrderListApiView.as_view()),
            path('<uuid:id>/delete/', order_views.OrderDeleteApiView.as_view()),
        ]
    )),
    path('dashboard/', include(
        [
            path('statistics/', dashboard_views.DashboardApiView.as_view()),
            path('recent_activity/', dashboard_views.RecentActivityApiView.as_view()),
        ]
    ))
]