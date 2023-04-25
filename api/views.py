import requests, time, uuid
from django.shortcuts import redirect
from django.http import Http404
from django.views import generic
from django.utils import timezone
from rest_framework import status
from django.db.models import F, Q
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from .models import Raffle, Ticket, Notification
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import cache_control
from rest_framework import generics, permissions, status
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .serializer import RaffleSerializer, TicketSerializer, RaffleUserSerializer, UserSerializer, NotificationSerializer



class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserTicketList(generics.ListAPIView):
    serializer_class = TicketSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(owner=user)

class UserRegistration(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [BasicAuthentication]

    def post(self, request, format=None):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserNotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user).order_by('-created_at')


class RaffleList(generics.ListAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @method_decorator(cache_control(max_age=3600))
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True, context={'request': request})
        return Response(serializer.data)
        
class RaffleDetail(generics.RetrieveAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class HotRaffle(generics.RetrieveAPIView):
    serializer_class = RaffleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        hot_raffles = Raffle.objects.filter(Q(tickets_available__gt=0) | Q(tickets_available=None)).order_by('-created_at')
        if hot_raffles:
            return hot_raffles[0]
        else:
            latest_raffle = Raffle.objects.latest('created_at')
            return latest_raffle


class TicketList(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketCreate(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the raffle object
        raffle = get_object_or_404(Raffle, id=request.data.get('raffle_id'))

        # Check if there are enough tickets available
        if raffle.tickets_available is None or raffle.tickets_available > 0:
            # Decrement available tickets and increment sold tickets
            raffle.tickets_available = F('tickets_available') - 1
            raffle.tickets_sold = F('tickets_sold') + 1
            raffle.save()

            # Create the ticket object
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user) # Set the owner field to the authenticated user
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'No more tickets available for this raffle.'}, status=status.HTTP_400_BAD_REQUEST)

class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.all().order_by('-created_at')



def paystack_payment(request, id):
    # Set up variables
    paystack_secret_key = 'sk_test_67e0a2056a3a4e3307026df87224d27ebccaa804'
    amount = 10000
    email = 'example@email.com'
    timestamp = str(int(time.time() * 1000))  # current timestamp in milliseconds
    unique_id = str(uuid.uuid4())  # unique identifier
    reference = timestamp + '_' + unique_id  # concatenate timestamp and unique id
    callback_url = request.build_absolute_uri('/paystack_callback/')


    request.session['ticket_ids'] = [int(id)]

    payload = {
        "email": email,
        "amount": amount,
        "reference": reference,
        "callback_url": callback_url
    }

    headers = {
        "Authorization": "Bearer " + paystack_secret_key,
        "Content-Type": "application/json"
    }


    response = requests.post('https://api.paystack.co/transaction/initialize', json=payload, headers=headers)
    authorization_url = response.json()['data']['authorization_url']

    return redirect(authorization_url)

def paystack_callback(request):
    reference = request.GET.get('reference')

    paystack_secret_key = 'sk_test_67e0a2056a3a4e3307026df87224d27ebccaa804'
    headers = {
        "Authorization": "Bearer " + paystack_secret_key,
        "Content-Type": "application/json"
    }


    verify_response = requests.get('https://api.paystack.co/transaction/verify/{}'.format(reference), headers=headers)
    status = verify_response.json()['data']['status']

    if status == 'success':
        ticket_ids = request.session.get('ticket_ids')
        admin = request.session.get('admin')
        if ticket_ids:
            tickets = Ticket.objects.filter(id__in=ticket_ids)
            for ticket in tickets:
                ticket.paid = True
                ticket.paystack_reference = reference
                ticket.save()

        if admin == "admin":
            return redirect(reverse('admin:api_ticket_changelist'))
        else:
            return HttpResponse('successful')
    else:
        return HttpResponse('Payment failed.')
