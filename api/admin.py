from django import forms
from django.urls import reverse
from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from django.utils.html import format_html
from .models import Raffle, Ticket, Notification
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ['created_at']
    search_fields = ('user__username', 'message')
    readonly_fields = ['created_at']

class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['key']  # exclude the 'key' field from the form

    def clean(self):
        cleaned_data = super().clean()
        raffle = cleaned_data.get('raffle')
        if raffle and raffle.tickets_available is not None and raffle.tickets_available <= 0:
            raise ValidationError(_('No more tickets available for this raffle.'))
        return cleaned_data

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_link', 'raffle_link', 'key_link')
    form = TicketAdminForm

    def owner_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.owner.id])
        return format_html('<a href="{}">{}</a>', url, obj.owner.username)
    owner_link.short_description = 'Owner'

    def raffle_link(self, obj):
        url = reverse('admin:api_raffle_change', args=[obj.raffle.id])
        return format_html('<a href="{}">{}</a>', url, obj.raffle.name)
    raffle_link.short_description = 'Raffle'

    def key_link(self, obj):
        url = reverse('admin:api_ticket_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.key)
    key_link.short_description = 'Key'


class RaffleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_link', 'tickets_sold_link', 'winner_link')
    actions = ['choose_winner']

    def has_delete_permission(self, request, obj=None):
        return True

    def name_link(self, obj):
        url = reverse('admin:api_raffle_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.name)

    def tickets_sold_link(self, obj):
        url = reverse('admin:api_ticket_changelist')
        return format_html('<a href="{}?raffle__id__exact={}">{}</a>', url, obj.id, obj.tickets_sold)

    def winner_link(self, obj):
        if obj.winner is None:
            return '-'
        url = reverse('admin:auth_user_change', args=[obj.winner.id])
        return format_html('<a href="{}">{}</a>', url, obj.winner.username)

    def choose_winner(self, request, queryset):
        for raffle in queryset:
            if raffle.winner is not None:
                messages.error(request, f"{raffle.name} already has a winner.")
                continue

            if raffle.tickets_sold < raffle.tickets_available:
                messages.error(request, f"Not enough tickets sold for {raffle.name}.")
                continue

            # Choose the winner randomly from the sold tickets
            sold_tickets = raffle.tickets.all()
            if sold_tickets.exists():
                winner_ticket = sold_tickets.order_by('?').first()
                raffle.winner = winner_ticket.owner
                raffle.save()
                messages.success(request, f"{raffle.name} winner is {raffle.winner.username}.")
            else:
                messages.error(request, f"No tickets sold for {raffle.name}.")

    name_link.short_description = "Name"
    tickets_sold_link.short_description = 'Tickets sold'
    winner_link.short_description = 'Winner'
    choose_winner.short_description = "Choose winner for selected raffles"


admin.site.register(Raffle, RaffleAdmin)
admin.site.register(Ticket, TicketAdmin)
