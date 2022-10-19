from django.contrib import admin
from users import models


@admin.register(models.User)
class User(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name')
    search_fields = ('username',)
