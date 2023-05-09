import random, uuid, string
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import F, Value
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_delete


letters_digits = string.ascii_letters + string.digits
symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?'
words = ['apple', 'banana', 'cherry', 'orange', 'mango', 'pear', 'peach']

def generate_key(length=60):
    key = ''.join(random.choice(letters_digits + symbols + ''.join(words)) for _ in range(length))
    return key

class Raffle(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ticket_price = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/')
    tickets_available = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def clean(self):
        if self.tickets_available != None and self.tickets_available < self.tickets_sold:
            raise ValidationError("Tickets sold cannot be greater than tickets available.")
    
    def save(self, *args, **kwargs):
        if self.pk:
            orig = Raffle.objects.get(pk=self.pk)
            if self.tickets_available > orig.tickets_available:
                self.winner = None
        super().save(*args, **kwargs)

    def set_winner(self):
        if self.tickets_available == 0 and not self.winner:
            ticket_owners = self.tickets.values_list('owner', flat=True)
            winner_id = random.choice(ticket_owners)
            print(winner_id)
            winner = User.objects.get(pk=winner_id)
            self.winner = winner
            self.end_date = timezone.now()
            self.save()

class Ticket(models.Model):
    key = models.CharField(max_length=13, unique=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='tickets')
    paystack_reference = models.CharField(max_length=255, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = generate_key()
        if self.pk is None:
            if self.raffle.tickets_available > 0:
                self.raffle.tickets_available -= 1
                self.raffle.tickets_sold += 1
                if self.raffle.tickets_available == 0:
                    self.raffle.set_winner()
                self.raffle.save()
        super().save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_delete, sender=Ticket)
def update_raffle_tickets(sender, instance, **kwargs):
    instance.raffle.tickets_available += 1
    instance.raffle.tickets_sold -= 1
    instance.raffle.save()

@receiver(pre_delete, sender=Raffle)
def delete_related_tickets(sender, instance, **kwargs):
    instance.tickets.all().delete()

@receiver(pre_delete, sender=Ticket)
def delete_ticket_notification(sender, instance, **kwargs):
    Notification.objects.create(user=instance.owner, message=f"Your ticket id ({instance.id}) for the {instance.raffle.name} raffle has been deleted.")

