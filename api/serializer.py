from rest_framework import serializers
from .models import Raffle, Ticket, Notification
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RaffleSerializer(serializers.ModelSerializer):
    tickets_owned = serializers.SerializerMethodField()

    class Meta:
        model = Raffle
        fields = '__all__'
        read_only_fields = ['id', 'tickets_sold', 'tickets_owned']

    def get_tickets_owned(self, obj):
        user = self.context['request'].user
        tickets = Ticket.objects.filter(raffle=obj, owner=user)
        return tickets.count()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    raffle = RaffleSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id']


class TicketUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'key']

class RaffleUserSerializer(serializers.ModelSerializer):
    tickets = TicketUserSerializer(many=True, read_only=True)

    class Meta:
        model = Raffle
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user
        if user.is_authenticated:
            tickets = instance.tickets.filter(owner=user)
        return representation
