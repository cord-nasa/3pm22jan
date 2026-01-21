from rest_framework import serializers
# Add this import at the top of serializer.py
from django.db.models import Avg, Count
from CordApp.models import*

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginTable
        fields = ['Username', 'Password', 'UserType']


class AddBookingSerializer(serializers.ModelSerializer):
    # Add the ImageField here to allow the POST request to save the file
    ParcelImage = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = BookingTable
        fields = ['PickupLocation', 'DropLocation', 'TRAVELERID', 'ParcelImage']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['id', 'Name', 'PhoneNo', 'Email', 'Place','ProfilePhoto']

class BookingSerializer(serializers.ModelSerializer):
    """
    Used by VerifyRideBookingAPI. 
    Matches the fields expected by 'VerifyPickupDropPage' in Flutter.
    """
    # Use dot walking to get the Requester's info
    Name = serializers.CharField(source='USERID.Name', default="Requester")
    PhoneNo = serializers.CharField(source='USERID.PhoneNo', default="")
    
    # Get Route details from the traveler's route
    StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', read_only=True)
    Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0)
    spaceavailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A")
    RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride")
    ParcelImage = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BookingTable
        fields = [
            'id', 'PickupLocation', 'DropLocation', 'RideType', 
            'TRAVELERID', 'PhoneNo', 'Name', 'StartingTime', 
            'Amount', 'spaceavailability', 'BookingStatus', 'ParcelImage'
        ]

class BookingSerializer1(serializers.ModelSerializer):
    """ Used for Booking History and OTP visibility """
    RideAvailability = serializers.CharField(source='TRAVELERID.RideAvailability', default="N/A")
    SpaceAvailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A")
    Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0)
    RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride")
    StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', default="00:00:00")
    EndingTime = serializers.TimeField(source='TRAVELERID.EndingTime', default="00:00:00")
    StartLocation = serializers.CharField(source='TRAVELERID.StartLocation', default="")
    EndLocation = serializers.CharField(source='TRAVELERID.EndLocation', default="")
    Kms = serializers.FloatField(source='TRAVELERID.Kms', default=0.0)
    VehicleType = serializers.CharField(source='TRAVELERID.VehicleType', default="Sedan")
    
    # Matching lowercase 'd' as seen in your previous logs
    Startdate = serializers.DateField(source='TRAVELERID.StartDate', allow_null=True)
    Enddate = serializers.DateField(source='TRAVELERID.EndDate', allow_null=True)

    Name = serializers.CharField(source='TRAVELERID.TRAVELERID.Name', default="Eco Traveler")
    PhoneNo = serializers.CharField(source='TRAVELERID.TRAVELERID.PhoneNo', default="")
    # ADD THIS LINE:
    BagSize = serializers.CharField(source='TRAVELERID.BagSize', default="Standard Bag")


    class Meta:
        model = BookingTable
        fields = [
            'id', 'PickupLocation', 'DropLocation', 'BookingStatus', 'Amount', 
            'BookingDate', 'OtpCode', 'RideAvailability', 'SpaceAvailability', 
            'RideType', 'StartingTime', 'EndingTime', 'StartLocation', 'EndLocation', 
            'Name', 'PhoneNo', 'Kms', 'VehicleType', 'Startdate', 'Enddate', 'BagSize'
        ]


class ComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintsTable
        fields = ['USERID', 'BOOKINGID', 'Description', 'Reply', 'ComplaintDate']
class FeedbackSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(source='USERID.Name')
    class Meta:
        model = FeedbackTable
        fields = ['Name', 'BOOKINGID', 'Rating', 'Comment']

class SendFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackTable
        fields = ['BOOKINGID', 'Rating', 'Comment']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTable
        fields = ['USERID', 'BOOKINGID', 'TransactionType', 'Amount', 'TransactionDate']

class TravelRouteSerializer(serializers.ModelSerializer):

    drivername = serializers.CharField(source='TRAVELERID.Name')
    driverphone = serializers.CharField(source='TRAVELERID.PhoneNo')
    # For Chat navigation
    traveler_login_id = serializers.IntegerField(source='TRAVELERID.LOGIN.id', read_only=True)
    ProfilePhoto = serializers.SerializerMethodField()
    
    # Add these two new fields
    AverageRating = serializers.SerializerMethodField()
    ReviewCount = serializers.SerializerMethodField()

    class Meta:
        model = TravelRouteTable
        fields = '__all__' # Or list them out specifically

    def get_ProfilePhoto(self, obj):
        # obj is the TravelRouteTable instance
        # obj.TRAVELERID links to the UserTable
        if obj.TRAVELERID and obj.TRAVELERID.ProfilePhoto:
            return obj.TRAVELERID.ProfilePhoto.url
        return None

    def get_AverageRating(self, obj):
        # Calculate avg rating across all bookings for this traveler
        avg = FeedbackTable.objects.filter(
            BOOKINGID__TRAVELERID__TRAVELERID=obj.TRAVELERID
        ).aggregate(Avg('Rating'))['Rating__avg']
        return round(avg, 1) if avg else 0.0

    def get_ReviewCount(self, obj):
        # Count total reviews for this traveler
        return FeedbackTable.objects.filter(
            BOOKINGID__TRAVELERID__TRAVELERID=obj.TRAVELERID
        ).count() 

class AddTravelRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelRouteTable
        # FIX: Added the missing location and availability fields here
        fields = [
            'StartLocation', 'EndLocation', 'SpaceAvailability', 'RideAvailability',
            'StartingTime', 'EndingTime', 'RideType', 'Amount', 'Kms', 'VehicleType', 
            'StartDate', 'EndDate', 'BagSize'
        ]
class ChatSerializer(serializers.ModelSerializer):
    # We override the sender and receiver fields to return the LOGIN ID
    sender = serializers.ReadOnlyField(source='sender.LOGIN.id')
    receiver = serializers.ReadOnlyField(source='receiver.LOGIN.id')

    class Meta:
        model = ChatTable
        fields = ['id', 'message', 'date', 'sender', 'receiver']

class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserTable
        fields = '__all__'


        # jmut kmrx enhx brjx


       


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipTable
        fields = "__all__"

