from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def is_subscriber(self, author) -> bool:
        return Subscriber.objects.filter(user=self, author=author).exists()


class Subscriber(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='subscribers'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='user_is_not_author'
            )
        ]

    def __str__(self):
        return f'{self.user} following {self.author}'
