from rest_framework import serializers
from models import User, Subscriber
# from api import serializers


class SubscriberSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscriber
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

    def get_email(self, obj):
        return obj.author.email

    def get_id(self, obj):
        return obj.author.id

    def get_username(self, obj):
        return obj.author.username

    def get_first_name(self, obj):
        return obj.author.first_name

    def get_last_name(self, obj):
        return obj.author.last_name
