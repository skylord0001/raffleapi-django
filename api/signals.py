from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Raffle, Notification

@receiver(post_save, sender=Ticket)
def create_ticket_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.owner, message=f"You have purchased a ticket for {instance.raffle.name}.")

@receiver(post_save, sender=Raffle)
def create_raffle_notification(sender, instance, created, **kwargs):
    if not created and instance.winner:
        notified_users = set()
        notifications = []
        for ticket in instance.tickets.all():
            if ticket.owner not in notified_users:
                notifications.append(Notification(user=ticket.owner, message=f"The winner of raffle {instance.name} has been selected."))
                notified_users.add(ticket.owner)

        if notifications:
            Notification.objects.bulk_create(notifications)

        Notification.objects.create(user=instance.winner, message=f"You have won the raffle {instance.name}!")
