from django.urls import path
from api import views as api
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from website import views as website
from django.views.decorators.cache import cache_control
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', website.home, name='home'),
    path('about/', website.about, name='about'),
    path('contact/', website.contact, name='contact'),

    path('api/tickets/', api.TicketList.as_view(), name='ticket-list'),
    path('api/tickets/create/', api.TicketCreate.as_view(), name='ticket-create'),
    path('api/tickets/<int:pk>/', api.TicketDetail.as_view(), name='ticket-detail'),

    path('api/raffles/', api.RaffleList.as_view(), name='raffle-list'),
    path('api/raffles/hot/', api.HotRaffle.as_view(), name='hot-raffle'),
    path('api/raffles/<int:pk>/', api.RaffleDetail.as_view(), name='raffle-detail'),

    path('api/user/profile/', api.UserDetail.as_view(), name='user-profile'),
    path('api/user/register/', api.UserRegistration.as_view(), name='user-register'),
    path('api/user/profile/tickets/', api.UserTicketList.as_view(), name='user-ticket-list'),
    path('api/user/notifications/', api.UserNotificationList.as_view(), name='user-notification-list'),

    path('api/notifications/', api.NotificationList.as_view(), name='notification-list'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, view=cache_control(max_age=3600)(serve))
