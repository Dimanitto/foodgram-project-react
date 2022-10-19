from typing import Optional
from django.db.utils import IntegrityError
from rest_framework import permissions, authentication, status, generics
from rest_framework.views import APIView
from djoser.views import UserViewSet, TokenCreateView
from djoser.conf import settings
from djoser import utils

from api.pagination import CustomPagination
from .models import User, Subscriber
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .serializers import SubscriberSerializer, CustomCreateTokenSerializerTwo, CustomUserSerializer


class CustomTokenCreateView(TokenCreateView):
    serializer_class = CustomCreateTokenSerializerTwo
    permission_classes = (permissions.AllowAny, )

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_200_OK
        )


class CustomUserViewSet(UserViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        if self.action == 'me':
            return CustomUserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return []
        return super().get_permissions()

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


def check_recipes_limit(recipes_limit: str) -> Optional[int]:
    """Функция проверки query_params на корректность"""
    recipes_limit = recipes_limit.__str__()
    if recipes_limit.isdigit():
        if (recipes_limit := int(recipes_limit)) > 0:
            return recipes_limit


class SubscriberViewSet(generics.ListAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        user = self.request.user
        recipes_limit = self.request.query_params.get('recipes_limit')
        recipes_limit = check_recipes_limit(recipes_limit)
        qs = Subscriber.objects.filter(user=user)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'recipes_limit': recipes_limit})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)


class SubscribeViewSet(APIView):
    queryset = Subscriber.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriberSerializer
    lookup_field = 'id'

    def post(self, request, id: int):
        user = request.user

        recipes_limit = request.query_params.get('recipes_limit')
        recipes_limit = check_recipes_limit(recipes_limit)

        if Subscriber.objects.filter(user=user, author_id=id).exists():
            return Response(
                {
                    'error':
                        (f'Ошибка подписки. '
                         f'Автор "{id}" уже есть в подписках')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            subscribe = Subscriber.objects.create(user=user, author_id=id)
        except IntegrityError:
            return Response(
                {'error': 'Нельзя подписаться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(subscribe, context={'recipes_limit': recipes_limit})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id: int):
        user = request.user
        if not Subscriber.objects.filter(
                user=user, author_id=id).exists():
            return Response(
                {
                    'error':
                        (f'Ошибка отписки. '
                         f'Автора "{id}" нету в подписках')
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscriber.objects.filter(
                user=user, author_id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
