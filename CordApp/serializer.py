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
    # Use SerializerMethodField to ensure absolute Cloudinary URLs
    ProfilePhoto = serializers.SerializerMethodField()
    IdProof = serializers.SerializerMethodField()
    class Meta:
        model = UserTable
        fields = ['id', 'Name', 'PhoneNo', 'Email', 'Place','ProfilePhoto','IdProof','UpiId']

# class BookingSerializer(serializers.ModelSerializer):
#     """
#     Used by VerifyRideBookingAPI. 
#     Matches the fields expected by 'VerifyPickupDropPage' in Flutter.
#     """
#     # Use dot walking to get the Requester's info
#     Name = serializers.CharField(source='USERID.Name', default="Requester")
#     PhoneNo = serializers.CharField(source='USERID.PhoneNo', default="")
    
#     # Get Route details from the traveler's route
#     StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', read_only=True)
#     Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0)
#     spaceavailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A")
#     RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride")
#     ParcelImage = serializers.ImageField(required=False, allow_null=True)
#     # --- ADD THE NEW FIELDS HERE ---
#     # --- ADD THE NEW FIELDS HERE ---
#     PaymentProof = serializers.ImageField(required=False, allow_null=True)
#     PaymentStatus = serializers.CharField()  # Add this too
#     UTR = serializers.CharField(source='UTR', allow_null=True)  # Add this if you have UTR field
#     class Meta:
#         model = BookingTable
#         fields = [
#             'id', 'PickupLocation', 'DropLocation', 'RideType', 
#             'TRAVELERID', 'PhoneNo', 'Name', 'StartingTime', 
#             'Amount', 'spaceavailability', 'BookingStatus', 'ParcelImage','PaymentProof', 'PaymentStatus', 'UTR'  # Added the missing fiel
#         ]
# class BookingSerializer(serializers.ModelSerializer):
#     Name = serializers.CharField(source='USERID.Name', default="Requester")
#     PhoneNo = serializers.CharField(source='USERID.PhoneNo', default="")
#     StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', read_only=True)
#     Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0)
#     spaceavailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A")
#     RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride")
    
#     # Use SerializerMethodField for images to guarantee absolute URLs
#     ParcelImage = serializers.SerializerMethodField()
#     PaymentProof = serializers.SerializerMethodField()
#     PaymentStatus = serializers.CharField(default="Pending") 
#     UTR = serializers.CharField(required=False, allow_null=True) 

#     class Meta:
#         model = BookingTable
#         fields = [
#             'id', 'PickupLocation', 'DropLocation', 'RideType', 
#             'TRAVELERID', 'PhoneNo', 'Name', 'StartingTime', 
#             'Amount', 'spaceavailability', 'BookingStatus', 
#             'ParcelImage', 'PaymentProof', 'PaymentStatus', 'UTR'
#         ]

#     def get_ParcelImage(self, obj):
#         if obj.ParcelImage:
#             return obj.ParcelImage.url
#         return None

#     def get_PaymentProof(self, obj):
#         if obj.PaymentProof:
#             return obj.PaymentProof.url
#         return None


    Name = serializers.CharField(source='USERID.Name', default="Requester")
    PhoneNo = serializers.CharField(source='USERID.PhoneNo', default="")
    StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', read_only=True)
    Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0)
    spaceavailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A")
    RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride")
    
    # 1. Use SerializerMethodField for absolute URLs
    ParcelImage = serializers.SerializerMethodField()
    PaymentProof = serializers.SerializerMethodField()
    PaymentStatus = serializers.CharField(default="Pending") 
    UTR = serializers.CharField(required=False, allow_null=True) 

    class Meta:
        model = BookingTable
        fields = [
            'id', 'PickupLocation', 'DropLocation', 'RideType', 
            'TRAVELERID', 'PhoneNo', 'Name', 'StartingTime', 
            'Amount', 'spaceavailability', 'BookingStatus', 
            'ParcelImage', 'PaymentProof', 'PaymentStatus', 'UTR'
        ]

    # 2. These methods return the Cloudinary URL directly
    def get_ParcelImage(self, obj):
        if obj.ParcelImage:
            return obj.ParcelImage.url # This is already https://res.cloudinary...
        return None

    def get_PaymentProof(self, obj):
        if obj.PaymentProof:
            return obj.PaymentProof.url
        return None
    
    
class BookingSerializer1(serializers.ModelSerializer):
    """ Used for Booking History and OTP visibility - Safe Version """
    RideAvailability = serializers.CharField(source='TRAVELERID.RideAvailability', default="N/A", read_only=True)
    SpaceAvailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A", read_only=True)
    Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0, read_only=True)
    RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride", read_only=True)
    StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', default="00:00:00", read_only=True)
    EndingTime = serializers.TimeField(source='TRAVELERID.EndingTime', default="00:00:00", read_only=True)
    StartLocation = serializers.CharField(source='TRAVELERID.StartLocation', default="", read_only=True)
    EndLocation = serializers.CharField(source='TRAVELERID.EndLocation', default="", read_only=True)
    Kms = serializers.FloatField(source='TRAVELERID.Kms', default=0.0, read_only=True)
    VehicleType = serializers.CharField(source='TRAVELERID.VehicleType', default="Sedan", read_only=True)
    
    # Path: Booking -> Route -> Traveler User -> Name
    Name = serializers.CharField(source='TRAVELERID.TRAVELERID.Name', default="Eco Traveler", read_only=True)
    PhoneNo = serializers.CharField(source='TRAVELERID.TRAVELERID.PhoneNo', default="", read_only=True)
    BagSize = serializers.CharField(source='TRAVELERID.BagSize', default="Standard", read_only=True)

    class Meta:
        model = BookingTable
        fields = [
            'id', 'PickupLocation', 'DropLocation', 'BookingStatus', 'Amount', 
            'BookingDate', 'OtpCode', 'RideAvailability', 'SpaceAvailability', 
            'RideType', 'StartingTime', 'EndingTime', 'StartLocation', 'EndLocation', 
            'Name', 'PhoneNo', 'Kms', 'VehicleType', 'BagSize', 'PaymentStatus'
        ]


# class BookingSerializer(serializers.ModelSerializer):
#     Name = serializers.CharField(source='USERID.Name', default="Requester")
#     PhoneNo = serializers.CharField(source='USERID.PhoneNo', default="")
#     StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', read_only=True)
#     Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0)
#     spaceavailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A")
#     RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride")
    
#     # Absolute URLs for Cloudinary
#     ParcelImage = serializers.SerializerMethodField()
#     PaymentProof = serializers.SerializerMethodField()
    
#     # Ensure PaymentStatus can be read correctly
#     PaymentStatus = serializers.CharField(default="Pending") 
#     UTR = serializers.CharField(required=False, allow_null=True) 

#     class Meta:
#         model = BookingTable
#         fields = [
#             'id', 'PickupLocation', 'DropLocation', 'RideType', 
#             'TRAVELERID', 'PhoneNo', 'Name', 'StartingTime', 
#             'Amount', 'spaceavailability', 'BookingStatus', 
#             'ParcelImage', 'PaymentProof', 'PaymentStatus', 'UTR'
#         ]

#     def get_ParcelImage(self, obj):
#         return obj.ParcelImage.url if obj.ParcelImage else None

#     def get_PaymentProof(self, obj):
#         return obj.PaymentProof.url if obj.PaymentProof else None

class BookingSerializer(serializers.ModelSerializer):
    # Dot walking: Accesses UserTable via USERID
    Name = serializers.CharField(source='USERID.Name', default="Requester", read_only=True)
    PhoneNo = serializers.CharField(source='USERID.PhoneNo', default="", read_only=True)
    
    # Dot walking: Accesses TravelRouteTable via TRAVELERID
    StartingTime = serializers.TimeField(source='TRAVELERID.StartingTime', read_only=True, allow_null=True)
    Amount = serializers.FloatField(source='TRAVELERID.Amount', default=0.0, read_only=True)
    spaceavailability = serializers.CharField(source='TRAVELERID.SpaceAvailability', default="N/A", read_only=True)
    RideType = serializers.CharField(source='TRAVELERID.RideType', default="Ride", read_only=True)
    
    ParcelImage = serializers.SerializerMethodField()
    PaymentProof = serializers.SerializerMethodField()
    
    PaymentStatus = serializers.CharField(default="Pending") 
    UTR = serializers.CharField(required=False, allow_null=True) 

    class Meta:
        model = BookingTable
        fields = [
            'id', 'PickupLocation', 'DropLocation', 'RideType', 
            'TRAVELERID', 'PhoneNo', 'Name', 'StartingTime', 
            'Amount', 'spaceavailability', 'BookingStatus', 
            'ParcelImage', 'PaymentProof', 'PaymentStatus', 'UTR'
        ]

    # SAFE CLOUDINARY URL ACCESS
    def get_ParcelImage(self, obj):
        try:
            # Check if the file exists and has an attribute 'url'
            if obj.ParcelImage and hasattr(obj.ParcelImage, 'url'):
                return obj.ParcelImage.url
        except Exception:
            pass
        return None

    def get_PaymentProof(self, obj):
        try:
            if obj.PaymentProof and hasattr(obj.PaymentProof, 'url'):
                return obj.PaymentProof.url
        except Exception:
            pass
        return None

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
    drivername = serializers.CharField(source='TRAVELERID.Name', read_only=True)
    driverphone = serializers.CharField(source='TRAVELERID.PhoneNo', read_only=True)
    traveler_login_id = serializers.IntegerField(source='TRAVELERID.LOGIN.id', read_only=True)
    
    # These must be MethodFields because the photos are in the UserTable, not TravelRouteTable
    ProfilePhoto = serializers.SerializerMethodField()
    AverageRating = serializers.SerializerMethodField()
    ReviewCount = serializers.SerializerMethodField()

    class Meta:
        model = TravelRouteTable
        fields = '__all__'

    def get_ProfilePhoto(self, obj):
        # Access the photo via the TRAVELERID relation safely
        try:
            if obj.TRAVELERID and obj.TRAVELERID.ProfilePhoto:
                return obj.TRAVELERID.ProfilePhoto.url
        except Exception:
            pass
        return None
    
    def get_AverageRating(self, obj):
        try:
            # Aggregate ratings for the specific traveler
            avg = FeedbackTable.objects.filter(
                BOOKINGID__TRAVELERID__TRAVELERID=obj.TRAVELERID
            ).aggregate(Avg('Rating'))['Rating__avg']
            return round(avg, 1) if avg else 0.0
        except Exception:
            return 0.0

    def get_ReviewCount(self, obj):
        try:
            return FeedbackTable.objects.filter(
                BOOKINGID__TRAVELERID__TRAVELERID=obj.TRAVELERID
            ).count()
        except Exception:
            return 0




# class TravelRouteSerializer(serializers.ModelSerializer):
#     drivername = serializers.CharField(source='TRAVELERID.Name')
#     driverphone = serializers.CharField(source='TRAVELERID.PhoneNo')
#     traveler_login_id = serializers.IntegerField(source='TRAVELERID.LOGIN.id', read_only=True)
#     ProfilePhoto = serializers.SerializerMethodField()
#     AverageRating = serializers.SerializerMethodField()
#     ReviewCount = serializers.SerializerMethodField()

#     class Meta:
#         model = TravelRouteTable
#         fields = '__all__'

#     def get_ProfilePhoto(self, obj):
#         if obj.ProfilePhoto:
#             return obj.ProfilePhoto.url  # Returns the full HTTPS Cloudinary link
#         return None
    
#     def get_IdProof(self, obj):
#         if obj.IdProof:
#             return obj.IdProof.url
#         return None
    
#     def get_AverageRating(self, obj):
#         # Calculate avg rating across all bookings for this traveler
#         avg = FeedbackTable.objects.filter(
#             BOOKINGID__TRAVELERID__TRAVELERID=obj.TRAVELERID
#         ).aggregate(Avg('Rating'))['Rating__avg']
#         return round(avg, 1) if avg else 0.0

#     def get_ReviewCount(self, obj):
#         # Count total reviews for this traveler
#         return FeedbackTable.objects.filter(
#             BOOKINGID__TRAVELERID__TRAVELERID=obj.TRAVELERID
#         ).count() 

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

