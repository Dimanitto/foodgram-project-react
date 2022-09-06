from django.urls import include, path
from . import views
# from users import views
# from views import SubscriberViewSet
from rest_framework.routers import DefaultRouter


app_name = 'users'

router = DefaultRouter()
router.register('users/subscriptions/', views.SubscriberViewSet, basename='subscriptions')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    # path('users/subscriptions/', )
]
