import email
import stripe
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages

from CordApp.models import *
from CordApp.serializer import *

from rest_framework import status
from rest_framework.views import APIView


from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .views import *
# Create your views here.

class LoginPage(View):
    def get(self, request):
        return render(request, "login.html")
    def post (self, request):
        username =request.POST['username']
        password = request.POST['password']
        try:
            login_obj=LoginTable.objects.get(Username=username,Password=password)
            if login_obj.UserType=='admin':
                return HttpResponse('''<script>alert("Welcome to Admin Panel");window.location="/adminhome";</script>''')
        except LoginTable.DoesNotExist:
                return HttpResponse('''<script>alert("Invalid Credentials");window.location="/";</script>''')

    
class viewuserpage(View):
    def get(self, request):
        user_obj = UserTable.objects.all()
        return render(request, "user.html", {'val': user_obj})

class ApproveUser(View):
    def get(self, request, lid):
        login_obj = LoginTable.objects.get(id=lid)
        login_obj.UserType = "user"
        login_obj.save()
        return redirect('viewuserpage')

class RejectUser(View):
    def get(self, request, lid):
        login_obj = LoginTable.objects.get(id=lid)
        login_obj.UserType = "reject"
        login_obj.save()
        return redirect('viewuserpage')

class viewbookingpage(View):
    def get(self, request):
        booking_obj = BookingTable.objects.all() 
        return render(request, "viewbooking.html", {'val': booking_obj})
    
class viewcomplaintpage(View):
    def get(self, request):
        complaints_obj = ComplaintsTable.objects.all()
        return render(request, "viewcomplaint.html",{'val': complaints_obj})
    
class SendReply(View):
    def post(self, request, cid):
        complaints_obj = ComplaintsTable.objects.get(id=cid)
        complaints_obj.Reply = request.POST['reply']
        complaints_obj.save()
        return redirect('viewcomplaintpage')
    
class viewfeedbackpage(View):
    def get(self, request):
        feedback_obj = FeedbackTable.objects.all()
        return render(request, "viewfeedback.html",{'val': feedback_obj})

class viewtrippage(View):
    def get( self, request):
        payment_obj = PaymentTable.objects.all()
        return render(request, "viewtrip.html",{'val': payment_obj}) 
    
class adminhome(View):
    def get( self, request):
        admin_obj = TravelRouteTable.objects.all()
        return render(request, "admin_home.html",{'val': admin_obj})
    

##########################API#############################

class LoginAPI(APIView):
    def post(self, request):
        print("###############")
        response_dict = {}


        username = request.data.get("username")
        password = request.data.get("Password")
        print("$$$$$$$$$$$$$$", username)
        print("$$$$$$$$$$$$$$", password)
        if not username or not password:
            response_dict["message"] = "Failed"
            return Response(response_dict,  status=status.HTTP_400_BAD_REQUEST)
        t_user = LoginTable.objects.filter(Username=username, Password=password).first()
        print("$$$$$$$$$$$", t_user)
        
        if not t_user:
            response_dict["message"] = "Failed"
            return Response(response_dict, status=status.HTTP_404_NOT_FOUND)
        
        else:
            response_dict["message"] = "Success"
            print("$$$$$$$$$$$",   t_user.id)
            response_dict["login_id"] = t_user.id
            response_dict["userrole"] = t_user.UserType
            print("response_dict", response_dict)
            return Response(response_dict, status=status.HTTP_200_OK)
        
from rest_framework.response import Response
        


# /////////////////////////////////////// USER API //////////////////////////////////////


class UserReg(APIView):
    def post(self,request):
        print("######### User Registration API #########ngr", request.data)
        user_serial = UserSerializer(data=request.data)
        login_serial = LoginSerializer(data=request.data)

        data_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
            login_profile = login_serial.save()
            user_profile = user_serial.save(LOGIN=login_profile)

            return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(user_serial.errors, status=status.HTTP_400_BAD_REQUEST)

# API to view travel routes
class ViewRideTravelRouteAPI(APIView):
    def get(self, request):
        e=TravelRouteTable.objects.filter(RideType='Ride')
        serializer=TravelRouteSerializer(e,many=True)
        print("#########", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
 #API to book ride or parcel   
class ViewParcelTravelRouteAPI(APIView):
    def get(self, request):
        b=TravelRouteTable.objects.filter(RideType='Parcel')
        serializer=TravelRouteSerializer(b,many=True)
        print("#########", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


import random

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

# class BookingAPI(APIView):
#     def post(self, request):
#         print("######### Parcel Booking API #########", request.data)
#         serializer = AddBookingSerializer(data=request.data)
#         try:
#             user = UserTable.objects.get(LOGIN__id=request.data.get('USERID'))
#             email = user.Email
#         except UserTable.DoesNotExist:
#             return Response(
#                 {"error": "Invalid USERID"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if serializer.is_valid():
#             otp = generate_otp()   # 🔐 Generate OTP

#             booking = serializer.save(
#                 USERID=user,
#                 BookingStatus='Pending',
#                 OtpCode=otp          # ✅ Store OTP
#             )
#             try:
#                 # Send email (Consider replacing this with a password reset link)
#                 send_mail(
#                     'OTP',
#                     f'Your Booking is: {booking.id } otp :-{otp}',
#                     'saanandsdb@gmail.com',  # From email
#                     [email],
#                 )
#                 print("Email sent successfully to -----------------", email)
#             except:   
#                 return Response({"message": "Booking created successfully", "otp": otp},status=status.HTTP_404_NOT_FOUND)
 


#             return Response(
#                 {
#                     "message": "Booking created successfully",
#                     "booking_id": booking.id,
#                     "otp": otp        # (Optional: remove in production)
#                 },
#                 status=status.HTTP_200_OK
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # API to view parcel bookings
# class ViewBookingHistoryAPI(APIView):    
#     def get(self, request, lid):
#         print("######### View Booking History API #########ngr", lid)
#         g=BookingTable.objects.filter(USERID__LOGIN_id=lid)
#         serializer=BookingSerializer1(g,many=True)
#         print("#########", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)    
    

class BookingAPI(APIView):
    def post(self, request):
        print("######### Parcel Booking API #########")
        # DRF combines request.POST and request.FILES into request.data
        print("FILES IN REQUEST:", request.FILES) 
        
        serializer = AddBookingSerializer(data=request.data)
        
        try:
            user = UserTable.objects.get(LOGIN__id=request.data.get('USERID'))
            email = user.Email
        except UserTable.DoesNotExist:
            return Response({"error": "Invalid USERID"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            otp = generate_otp()
            # The image will be saved automatically because it's part of request.data
            booking = serializer.save(
                USERID=user,
                BookingStatus='Pending',
                OtpCode=otp
            )
            
            # Email Logic
            try:
                send_mail(
                    'OTP',
                    f'Your Booking ID is: {booking.id}. OTP: {otp}',
                    'saanandsdb@gmail.com',
                    [email],
                )
            except:
                pass

            return Response({
                "message": "Booking created successfully",
                "booking_id": booking.id,
                "otp": otp
            }, status=status.HTTP_201_CREATED)

        print("SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# /////////////////////////////////////// Traveler API //////////////////////////////////////


# CordApp/views.py

class ViewBookingHistoryAPI(APIView):    
    def get(self, request, lid):
        print("######### View Booking History API ######### lid:", lid)
        # Filters bookings where the user is the one who made the request
        bookings = BookingTable.objects.filter(USERID__LOGIN_id=lid)
        
        # Ensure BookingSerializer1 includes 'ParcelImage' in its Meta fields
        serializer = BookingSerializer1(bookings, many=True)
        
        print("Serialized History data:", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)









# API to view nearest travelers
class NearestTravelersAPI(APIView):
    def get(self, request):
        a=UserTable.objects.all()
        serializer=UserSerializer(a,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
 


class ComplaintReplyAPI(APIView):

    def get(self, request, lid):
        complaints = ComplaintsTable.objects.filter(USERID__LOGIN_id=lid)
        serializer = ComplaintsSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, lid):
        try:
            user_obj = UserTable.objects.get(LOGIN__id=lid)

            booking_id = request.data.get('BOOKINGID')
            booking_obj = BookingTable.objects.get(id=booking_id)

            complaint_obj = ComplaintsTable(
                USERID=user_obj,
                BOOKINGID=booking_obj,
                Description=request.data.get('Description')
            )
            complaint_obj.save()

            serializer = ComplaintsSerializer(complaint_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except UserTable.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except BookingTable.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

# class    ComplaintReplyAPI(APIView):
#     def get(self, request, lid):
#         C=ComplaintsTable.objects.filter(USERID__LOGIN_id=lid)
#         serializer=ComplaintsSerializer(C,many=True)
#         print("#########", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self,request,lid):
#         print("######### Send Complaints API #########ngr", request.data)
#         user_obj = UserTable.objects.get(LOGIN__id=lid)
#         complaint_obj = ComplaintsTable()
#         # complaint_obj.Subject = request.data.get('Subject')
#         complaint_obj.USERID = user_obj
#         complaint_obj.BOOKINGID = request.data.get('BOOKINGID')
#         complaint_obj.Description = request.data.get('Description')
#         # complaint_obj.Reply = request.data.get('Reply')
#         complaint_obj.save()
#         serializer=ComplaintsSerializer(complaint_obj)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
 # API to view feedback and reply   
class FeedbackReplyAPI(APIView):
    def get(self, request):
        d=FeedbackTable.objects.all()
        serializer=FeedbackSerializer(d,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# API to view earnings
class ViewEarningsAPI(APIView):
    def get(self, request):
        h=PaymentTable.objects.all()
        serializer=PaymentSerializer(h,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# API to view feedbacks
class ViewFeedbackAPI(APIView):
    def get(self, request):
        i=FeedbackTable.objects.all()
        serializer=FeedbackSerializer(i,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SendComplaintsAPI(APIView):
    def post(self,request,id):
        guardian=BookingTable.objects.get(USERID=id)
        serializer=BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(guardian=guardian)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendFeedbackAPI(APIView):
    def get(self, request, id):
        c = FeedbackTable.objects.filter(BOOKINGID__TRAVELERID__TRAVELERID__LOGIN_id=id)
        d = FeedbackSerializer(c, many=True)
        print("#########", d.data)
        return Response(d.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        print("######### Add Feedback API #########", request.data)

        # 1️⃣ Get USER using login id
        user_obj = UserTable.objects.get(LOGIN__id=id)

        # 2️⃣ Get BOOKING (optional)
        booking_id = request.data.get('BOOKINGID')
        booking_obj = None
        if booking_id:
            booking_obj = BookingTable.objects.get(id=booking_id)

        # 3️⃣ CREATE feedback (NO .get())
        serializer = SendFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                USERID=user_obj,
                BOOKINGID=booking_obj
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddTravelRouteAPI(APIView):
    def post(self,request,id):
        print("######### Add Travel Route API #########ngr", request.data)
        print("######### A---------------r", id)
        TRAVELER=UserTable.objects.get(LOGIN_id=id)
        serializer=AddTravelRouteSerializer(data=request.data)
        if serializer.is_valid():
            print("######### B---------------r")
            serializer.save(TRAVELERID=TRAVELER)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyRideBookingAPI(APIView):
    def get(self, request, id): 
        print("######### Verify Ride Booking API ######### User ID:", id) 
        try:
            # We filter by following the relationship: 
            # Booking -> TravelRoute (TRAVELERID) -> User (TRAVELERID) -> Login (id)
            booking = BookingTable.objects.filter(TRAVELERID__TRAVELERID__LOGIN_id=id)
            
            if not booking.exists():
                print(f"No bookings found in database for User ID {id}")
                return Response({"error": "No booking found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Using the serializer that includes the ParcelImage field
            serializer = BookingSerializer(booking, many=True)
            
            print("Serialized data for Flutter: ", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error in Verify API:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class VerifyRideBookingAPI(APIView):
#     def get(self, request, id): 
#         print("######### Verify Ride Booking API #########ngr", id) 
#         # Changed from GET to POST for saving data
#         try:
            
#             booking = BookingTable.objects.filter(TRAVELERID__TRAVELERID__LOGIN_id=id)
#             print("Booking fetched: ", booking) 
#             if not booking:
#                 return Response({"error": "No booking found for this ID"}, status=status.HTTP_404_NOT_FOUND)
#             serializer = BookingSerializer(booking, many=True)
#             print("Serialized data:------------- ", serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
            

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyParcelBookingAPI(APIView):
    def post(self,request,id):
        guardian=BookingTable.objects.get(USERID=id)
        serializer=BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(guardian=guardian)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SendChatAPI(APIView):
#     def post(self, request):
#         print("######### Send Chat API #########ngr", request.data)
#         sender_id=request.data['sender_id']
#         receiver_id=request.data['receiver_id']
#         c= UserTable.objects.get(LOGIN__id=sender_id)
#         d = UserTable.objects.get(LOGIN__id=receiver_id)
#         chat = ChatTable.objects.create(
#             sender=c,
#             receiver=d,
#             message=request.data['message']
#         )
#         return Response(ChatSerializer(chat).data)

class SendChatAPI(APIView):
    def post(self, request):
        sender_id = request.data['sender_id']
        receiver_id = request.data['receiver_id']
        
        try:
            # Find User objects based on the Login ID sent from Flutter
            c = UserTable.objects.get(LOGIN__id=sender_id)
            d = UserTable.objects.get(LOGIN__id=receiver_id)
            
            ChatTable.objects.create(
                sender=c,
                receiver=d,
                message=request.data['message']
            )
            return Response({"status": "success"}, status=200)
        except UserTable.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=404)

from django.db.models import Q


class ViewChatAPI(APIView):
    def get(self, request, sender_id, receiver_id):
        try:
            sender_user = UserTable.objects.get(LOGIN__id=sender_id)
            receiver_user = UserTable.objects.get(LOGIN__id=receiver_id)

            chats = ChatTable.objects.filter(
                Q(sender=sender_user, receiver=receiver_user) |
                Q(sender=receiver_user, receiver=sender_user)
            ).order_by('date')

            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data, status=200)

        except UserTable.DoesNotExist:
            return Response({"error": "One or both users do not exist."}, status=404)


class ViewTraveller(APIView):
    def get(self, request):
        travelers = UserTable.objects.filter(LOGIN__UserType="traveler")
        serializer = UserTableSerializer(travelers, many=True)
        print("#########", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewUser(APIView):
    def get(self, request):
        travelers = UserTable.objects.filter(LOGIN__UserType="user")
        serializer = UserTableSerializer(travelers, many=True)
        print("#########", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VerifyOtp(APIView):
    def post(self, request, lid):
        print("======", request.data)
        booking_otp = request.data.get('otp')
        booking_id = request.data.get('booking_id')
        # try:
        print("======", booking_id)
        booking_obj = BookingTable.objects.get(id=booking_id)
        print("===otpdata==-----------------=", booking_obj.OtpCode)
        print("===type otp===", booking_otp)
        if booking_obj.OtpCode == booking_otp:
            booking_obj.BookingStatus = 'Verified'
            booking_obj.save()
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        # except BookingTable.DoesNotExist:
        #     return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)    
    
class reject_booking_api(APIView):
    def post(self, request):
        print("======", request.data)
        booking_id = request.data.get('booking_id')
        try:
            booking_obj = BookingTable.objects.get(id=booking_id)
            booking_obj.BookingStatus = 'Rejected'
            booking_obj.save()
            return Response({"message": "Booking rejected successfully"}, status=status.HTTP_200_OK)
        except BookingTable.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)







from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentTable, BookingTable

class CreatePaymentIntent(APIView):
    def post(self, request):
        print("######### Create Payment Intent API #########", request.data)
        
        # 1. Extract data from request
        data = request.data
        booking_id = data.get('booking_id')
        payment_method = data.get('payment_method')
        amount = data.get('amount')

        try:
            # 2. Handle the Booking instance
            # If booking_id is 0 or None, we set it to None (allowed by your model)
            booking_instance = None
            if booking_id and booking_id != 0:
                booking_instance = BookingTable.objects.get(id=booking_id)
                booking_instance.BookingStatus='paid'
                booking_instance.save()
            # 3. Create and Save the Payment record
            payment = PaymentTable.objects.create(
                BOOKINGID=booking_instance,
                TransactionType=payment_method,
                Amount=amount
            )

            return Response({
                "message": "Payment intent created successfully",
                "payment_id": payment.id
            }, status=status.HTTP_201_CREATED)

        except BookingTable.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateGratitudeAPI(APIView):
    def post(self, request):
        try:
            booking_id = request.data.get("BOOKINGID")
            tip_amount = request.data.get("GratitudeAmount")
            print("---------", request.data)
            booking = BookingTable.objects.get(id=booking_id)
            booking.BookingStatus='received'
            booking.save()
            # Save tip
            tip = TipTable.objects.create(
                BOOKING=booking,
                Tip=tip_amount
            )

            # Update booking status
            booking.PaymentStatus = "Tip Sent"
            booking.save()

            return Response({
                "status": "success",
                "message": "Gratitude added successfully",
                "tip_id": tip.id
            }, status=status.HTTP_200_OK)

        except BookingTable.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Invalid Booking ID"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


