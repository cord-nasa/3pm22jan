from django.db import models

# Create your models here.

class LoginTable(models.Model):
    Username = models.CharField(max_length=30, null=True, blank=True)
    Password = models.CharField(max_length=30, null=True, blank=True)
    UserType = models.CharField(max_length=30, null=True, blank=True)

class UserTable(models.Model):
    LOGIN = models.ForeignKey(LoginTable, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=30, null=True, blank=True)
    PhoneNo = models.BigIntegerField(null=True, blank=True)
    Email = models.CharField(max_length=30, null=True, blank=True)
    Place = models.CharField(max_length=30, null=True, blank=True)
    # ADD THIS LINE:
    ProfilePhoto = models.ImageField(upload_to='profiles/', null=True, blank=True)


# class TravelRouteTable(models.Model):
#     # USERID = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name="route_user", null=True, blank=True)
#     TRAVELERID = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name="route_traveler", null=True, blank=True)
#     StartLocation = models.CharField(max_length=300, null=True, blank=True)
#     EndLocation = models.CharField(max_length=300, null=True, blank=True)
#     # WayPoint = models.CharField(max_length=20, null=True, blank=True)
#     # Distance_Km = models.FloatField(null=True, blank=True)
#     StartingTime = models.TimeField(null=True, blank=True)
#     EndingTime = models.TimeField(null=True, blank=True)
#     Created_At = models.DateField(auto_now_add=True)
#     RideType = models.CharField(max_length=20, null=True, blank=True)
#     Amount=models.FloatField(null=True,blank=True)
#     SpaceAvailability = models.CharField(max_length=20, null=True, blank=True)
#     RideAvailability = models.CharField(max_length=20, null=True, blank=True)

class TravelRouteTable(models.Model):
    TRAVELERID = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name="route_traveler", null=True, blank=True)
    StartLocation = models.CharField(max_length=300, null=True, blank=True)
    EndLocation = models.CharField(max_length=300, null=True, blank=True)
    # Physics & Transparency Fields
    Kms = models.FloatField(default=0.0) 
    VehicleType = models.CharField(max_length=50, default="Sedan")
    StartDate = models.DateField(null=True, blank=True)
    EndDate = models.DateField(null=True, blank=True)
    
    StartingTime = models.TimeField(null=True, blank=True)
    EndingTime = models.TimeField(null=True, blank=True)
    RideType = models.CharField(max_length=20, null=True, blank=True) # "Ride" or "Parcel"
    Amount = models.FloatField(null=True, blank=True)
    SpaceAvailability = models.CharField(max_length=20, null=True, blank=True)
    RideAvailability = models.CharField(max_length=20, null=True, blank=True)
    # ADD THIS LINE:
    BagSize = models.CharField(max_length=50, null=True, blank=True, default="N/A")


class BookingTable(models.Model):
    USERID = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    TRAVELERID = models.ForeignKey(TravelRouteTable, on_delete=models.CASCADE, null=True, blank=True)
    PickupLocation = models.CharField(max_length=300, null=True, blank=True)
    DropLocation = models.CharField(max_length=300, null=True, blank=True)
    BookingStatus = models.CharField(max_length=20, default="Pending")
    BookingDate = models.DateField(auto_now_add=True, null=True, blank=True)
    OtpCode = models.CharField(max_length=10, null=True, blank=True)
    ParcelImage = models.ImageField(upload_to='parcel_pics/', null=True, blank=True)



class ComplaintsTable(models.Model):
    USERID = models.ForeignKey(UserTable,on_delete=models.CASCADE)
    BOOKINGID = models.ForeignKey(BookingTable, on_delete=models.CASCADE, null=True, blank=True)
    Description = models.CharField(max_length=300,null=True, blank=True)
    Reply = models.CharField(max_length=300, null=True,blank=True)
    ComplaintDate = models.DateField(auto_now_add=True)

class FeedbackTable(models.Model):
    USERID = models.ForeignKey(UserTable,on_delete=models.CASCADE)
    BOOKINGID = models.ForeignKey(BookingTable, on_delete=models.CASCADE, null=True, blank=True)
    Rating = models.FloatField(null=True,blank=True)
    Comment = models.CharField(max_length=500, null=True,blank=True)
    FeedbackDate = models.DateField(auto_now_add=True)


class PaymentTable(models.Model):
    BOOKINGID = models.ForeignKey(BookingTable, on_delete=models.CASCADE, null=True, blank=True)
    TransactionType = models.CharField(max_length=10, null=True, blank=True)
    Amount = models.FloatField(null=True, blank=True)
    TransactionDate = models.DateField(auto_now_add=True)
    
# models.py
class ChatTable(models.Model):
    sender = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserTable, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class TipTable(models.Model):
    BOOKING = models.ForeignKey(BookingTable, on_delete=models.CASCADE, null=True, blank=True)
    Tip = models.CharField(max_length=100, null=True, blank=True)
    Created_At = models.DateField(auto_now_add=True)




