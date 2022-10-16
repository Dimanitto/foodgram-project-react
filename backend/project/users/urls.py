from django.urls import include, path, re_path
from . import views
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter


app_name = 'users'

router = DefaultRouter()
router.register("users", views.CustomUserViewSet)

urlpatterns = [
    path('users/subscriptions/', views.SubscriberViewSet.as_view(), name='subscriptions'),
    path('users/<int:id>/subscribe/', views.SubscribeViewSet.as_view(), name='subscribe'),
    path('', include(router.urls)),
    re_path(r"^auth/token/login/?$", views.CustomTokenCreateView.as_view(), name="login"),
    re_path(r"^auth/token/logout/?$", TokenDestroyView.as_view(), name="logout"),
]
