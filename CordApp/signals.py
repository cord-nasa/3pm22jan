from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookingTable, NotificationTable

@receiver(post_save, sender=BookingTable)
def send_booking_notification(sender, instance, created, **kwargs):
    user = instance.USERID
    # instance.TRAVELERID points to TravelRouteTable, 
    # and TravelRouteTable.TRAVELERID points to the UserTable.
    traveler = instance.TRAVELERID.TRAVELERID 
    status = instance.BookingStatus

    if created:
        # 1. NOTIFY THE TRAVELER that someone booked their route
        NotificationTable.objects.create(
            USERID=traveler,
            Message=f"New Booking! {user.Name} has requested a {instance.TRAVELERID.RideType} to {instance.DropLocation}."
        )
    else:
        # 2. NOTIFY THE USER that the status changed (Accepted, Rejected, etc.)
        NotificationTable.objects.create(
            USERID=user,
            Message=f"Update: Your booking for {instance.DropLocation} is now {status}."
        )