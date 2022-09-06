from rest_framework import viewsets, permissions, authentication, status, generics, mixins
# from .models import User, Subscriber
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from serializers import SubscriberSerializer


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class SubscriberViewSet(ListCreateDeleteViewSet):
    # TODO  поменять на ListViewSet?
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    serializer_class = SubscriberSerializer

