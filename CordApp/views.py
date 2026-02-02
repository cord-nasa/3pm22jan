# import email
# import stripe
# from urllib import response
# from django.http import HttpResponse
# from django.shortcuts import redirect, render
# from django.views import View
# from django.core.mail import send_mail
# from django.shortcuts import redirect
# from django.contrib import messages

# from CordApp.models import *
# from CordApp.serializer import *

# from rest_framework import status
# from rest_framework.views import APIView


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.conf import settings
# from .views import *
# # Create your views here.

# class LoginPage(View):
#     def get(self, request):
#         return render(request, "login.html")
#     def post (self, request):
#         username =request.POST['username']
#         password = request.POST['password']
#         try:
#             login_obj=LoginTable.objects.get(Username=username,Password=password)
#             if login_obj.UserType=='admin':
#                 return HttpResponse('''<script>alert("Welcome to Admin Panel");window.location="/adminhome";</script>''')
#         except LoginTable.DoesNotExist:
#                 return HttpResponse('''<script>alert("Invalid Credentials");window.location="/";</script>''')

    
# class viewuserpage(View):
#     def get(self, request):
#         user_obj = UserTable.objects.all()
#         return render(request, "user.html", {'val': user_obj})

# class ApproveUser(View):
#     def get(self, request, lid):
#         login_obj = LoginTable.objects.get(id=lid)
#         login_obj.UserType = "user"
#         login_obj.save()
#         return redirect('viewuserpage')

# class RejectUser(View):
#     def get(self, request, lid):
#         login_obj = LoginTable.objects.get(id=lid)
#         login_obj.UserType = "reject"
#         login_obj.save()
#         return redirect('viewuserpage')

# class viewbookingpage(View):
#     def get(self, request):
#         booking_obj = BookingTable.objects.all() 
#         return render(request, "viewbooking.html", {'val': booking_obj})
    
# class viewcomplaintpage(View):
#     def get(self, request):
#         complaints_obj = ComplaintsTable.objects.all()
#         return render(request, "viewcomplaint.html",{'val': complaints_obj})
    
# class SendReply(View):
#     def post(self, request, cid):
#         complaints_obj = ComplaintsTable.objects.get(id=cid)
#         complaints_obj.Reply = request.POST['reply']
#         complaints_obj.save()
#         return redirect('viewcomplaintpage')
    
# class viewfeedbackpage(View):
#     def get(self, request):
#         feedback_obj = FeedbackTable.objects.all()
#         return render(request, "viewfeedback.html",{'val': feedback_obj})

# class viewtrippage(View):
#     def get( self, request):
#         payment_obj = PaymentTable.objects.all()
#         return render(request, "viewtrip.html",{'val': payment_obj}) 
    
# class adminhome(View):
#     def get( self, request):
#         admin_obj = TravelRouteTable.objects.all()
#         return render(request, "admin_home.html",{'val': admin_obj})
    

# ##########################API#############################

# class LoginAPI(APIView):
#     def post(self, request):
#         print("###############")
#         response_dict = {}


#         username = request.data.get("username")
#         password = request.data.get("Password")
#         print("$$$$$$$$$$$$$$", username)
#         print("$$$$$$$$$$$$$$", password)
#         if not username or not password:
#             response_dict["message"] = "Failed"
#             return Response(response_dict,  status=status.HTTP_400_BAD_REQUEST)
#         t_user = LoginTable.objects.filter(Username=username, Password=password).first()
#         print("$$$$$$$$$$$", t_user)
        
#         if not t_user:
#             response_dict["message"] = "Failed"
#             return Response(response_dict, status=status.HTTP_404_NOT_FOUND)
        
#         else:
#             response_dict["message"] = "Success"
#             print("$$$$$$$$$$$",   t_user.id)
#             response_dict["login_id"] = t_user.id
#             response_dict["userrole"] = t_user.UserType
#             print("response_dict", response_dict)
#             return Response(response_dict, status=status.HTTP_200_OK)
        
# from rest_framework.response import Response
        


# class UserReg(APIView):
#     def post(self, request):
#         print("######### User Registration API #########", request.data)
        
#         # request.data automatically includes files (request.FILES) when using Multipart/FormData
#         user_serial = UserSerializer(data=request.data)
#         login_serial = LoginSerializer(data=request.data)

#         if user_serial.is_valid() and login_serial.is_valid():
#             login_profile = login_serial.save()
#             # The serializer will now automatically handle ProfilePhoto and IdProof
#             user_profile = user_serial.save(LOGIN=login_profile)

#             return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        
#         print("User Errors:", user_serial.errors)
#         print("Login Errors:", login_serial.errors)
#         return Response(user_serial.errors, status=status.HTTP_400_BAD_REQUEST)

# # API to view travel routes
# class ViewRideTravelRouteAPI(APIView):
#     def get(self, request):
#         e=TravelRouteTable.objects.filter(RideType='Ride')
#         serializer=TravelRouteSerializer(e,many=True)
#         print("#########", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#  #API to book ride or parcel   
# class ViewParcelTravelRouteAPI(APIView):
#     def get(self, request):
#         b=TravelRouteTable.objects.filter(RideType='Parcel')
#         serializer=TravelRouteSerializer(b,many=True)
#         print("#########", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# import random

# def generate_otp():
#     return str(random.randint(100000, 999999))  # 6-digit OTP



# class BookingAPI(APIView):
#     def post(self, request):
#         print("######### Booking API #########")
#         # DRF combines request.POST and request.FILES into request.data
#         print("Data received:", request.data)
        
#         trav_id = request.data.get('TRAVELERID')
#         serializer = AddBookingSerializer(data=request.data)
        
#         # 1. Fetch the User (Sender)
#         try:
#             user = UserTable.objects.get(LOGIN__id=request.data.get('USERID'))
#             target_email = user.Email 
#         except UserTable.DoesNotExist:
#             return Response({"error": "Invalid USERID"}, status=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             otp = generate_otp()

#             # 2. Save the Booking first
#             booking = serializer.save(
#                 USERID=user,
#                 BookingStatus='Pending',
#                 OtpCode=otp
#             )
            
#             # 3. Determine Ride Type for Custom Email
#             try:
#                 # Fetch the route details to check RideType
#                 route_obj = TravelRouteTable.objects.get(id=trav_id)
#                 ride_type = route_obj.RideType # "Ride" or "Parcel"
                
#                 # Default values (Parcel)
#                 email_subject = 'Parcel Booking Confirmation & OTP'
#                 email_body = (
#                     f'Hello {user.Name},\n\n'
#                     f'Your parcel booking request has been received successfully.\n'
#                     f'Booking ID: {booking.id}\n'
#                     f'YOUR SECURE OTP: {otp}\n\n'
#                     f'Please share this OTP with the traveler ONLY when they pick up your parcel.'
#                 )

#                 # Custom message for Ride Booking
#                 if ride_type == "Ride":
#                     email_subject = 'Ride Booking Confirmation & OTP'
#                     email_body = (
#                         f'Hello {user.Name},\n\n'
#                         f'Your ride has been successfully booked.\n'
#                         f'Booking ID: {booking.id}\n'
#                         f'YOUR SECURE OTP: {otp}\n\n'
#                         f'Please share this OTP with the driver when you board the vehicle.'
#                     )

#                 # 4. Send the Dynamic Email
#                 send_mail(
#                     email_subject,
#                     email_body,
#                     'saanandsdb@gmail.com', # From Email
#                     [target_email],         # To User (Sender)
#                 )
#                 print(f"--- {ride_type} Confirmation Email Sent Successfully ---")

#             except Exception as e:
#                 print(f"--- EMAIL FAILED: {e} ---")

#             return Response({
#                 "message": "Booking created successfully",
#                 "booking_id": booking.id,
#                 "otp": otp
#             }, status=status.HTTP_201_CREATED)

#         print("SERIALIZER ERRORS:", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ViewBookingHistoryAPI(APIView):    
#     def get(self, request, lid):
#         print("######### View Booking History API ######### lid:", lid)
#         # Filters bookings where the user is the one who made the request
#         bookings = BookingTable.objects.filter(USERID__LOGIN_id=lid)
        
#         # Ensure BookingSerializer1 includes 'ParcelImage' in its Meta fields
#         serializer = BookingSerializer1(bookings, many=True)
        
#         print("Serialized History data:", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)









# # API to view nearest travelers
# class NearestTravelersAPI(APIView):
#     def get(self, request):
#         a=UserTable.objects.all()
#         serializer=UserSerializer(a,many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
 


# class ComplaintReplyAPI(APIView):

#     def get(self, request, lid):
#         complaints = ComplaintsTable.objects.filter(USERID__LOGIN_id=lid)
#         serializer = ComplaintsSerializer(complaints, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, lid):
#         try:
#             user_obj = UserTable.objects.get(LOGIN__id=lid)

#             booking_id = request.data.get('BOOKINGID')
#             booking_obj = BookingTable.objects.get(id=booking_id)

#             complaint_obj = ComplaintsTable(
#                 USERID=user_obj,
#                 BOOKINGID=booking_obj,
#                 Description=request.data.get('Description')
#             )
#             complaint_obj.save()

#             serializer = ComplaintsSerializer(complaint_obj)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except UserTable.DoesNotExist:
#             return Response(
#                 {"error": "User not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         except BookingTable.DoesNotExist:
#             return Response(
#                 {"error": "Booking not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )


    
#  # API to view feedback and reply   
# class FeedbackReplyAPI(APIView):
#     def get(self, request):
#         d=FeedbackTable.objects.all()
#         serializer=FeedbackSerializer(d,many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# from django.db.models import Sum
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import UserTable, TravelRouteTable, PaymentTable

# class ViewEarningsAPI(APIView):
#     def get(self, request, lid):
#         try:
#             # Get the Traveler based on login ID
#             traveler = UserTable.objects.get(LOGIN_id=lid)
            
#             # Calculate Total Kms (from all routes published by this traveler)
#             total_kms = TravelRouteTable.objects.filter(TRAVELERID=traveler).aggregate(Sum('Kms'))['Kms__sum'] or 0.0
            
#             # Calculate Total Gross Earnings (from all payments received for their bookings)
#             total_earned = PaymentTable.objects.filter(
#                 BOOKINGID__TRAVELERID__TRAVELERID=traveler
#             ).aggregate(Sum('Amount'))['Amount__sum'] or 0.0
            
#             # Logic: Carbon Credits (10 CC per KM)
#             carbon_credits = int(total_kms * 10)
            
#             # Get Recent Activity (History)
#             recent_payments = PaymentTable.objects.filter(
#                 BOOKINGID__TRAVELERID__TRAVELERID=traveler
#             ).order_by('-TransactionDate')[:10]
            
#             history_data = []
#             for p in recent_payments:
#                 history_data.append({
#                     "id": f"TRN-{p.id}",
#                     "type": p.BOOKINGID.TRAVELERID.RideType,
#                     "amount": p.Amount,
#                     "date": p.TransactionDate.strftime("%d-%m-%Y"),
#                     "ccEarned": int((p.BOOKINGID.TRAVELERID.Kms or 0) * 10)
#                 })

#             return Response({
#                 "total_kms": round(total_kms, 2),
#                 "total_earned": round(total_earned, 2),
#                 "carbon_credits": carbon_credits,
#                 "recent_activity": history_data
#             }, status=status.HTTP_200_OK)

#         except UserTable.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
# # API to view feedbacks
# class ViewFeedbackAPI(APIView):
#     def get(self, request):
#         i=FeedbackTable.objects.all()
#         serializer=FeedbackSerializer(i,many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class SendComplaintsAPI(APIView):
#     def post(self,request,id):
#         guardian=BookingTable.objects.get(USERID=id)
#         serializer=BookingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(guardian=guardian)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SendFeedbackAPI(APIView):
#     def get(self, request, id):
#         c = FeedbackTable.objects.filter(BOOKINGID__TRAVELERID__TRAVELERID__LOGIN_id=id)
#         d = FeedbackSerializer(c, many=True)
#         print("#########", d.data)
#         return Response(d.data, status=status.HTTP_200_OK)

#     def post(self, request, id):
#         print("######### Add Feedback API #########", request.data)

#         # 1️⃣ Get USER using login id
#         user_obj = UserTable.objects.get(LOGIN__id=id)

#         # 2️⃣ Get BOOKING (optional)
#         booking_id = request.data.get('BOOKINGID')
#         booking_obj = None
#         if booking_id:
#             booking_obj = BookingTable.objects.get(id=booking_id)

#         # 3️⃣ CREATE feedback (NO .get())
#         serializer = SendFeedbackSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(
#                 USERID=user_obj,
#                 BOOKINGID=booking_obj
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         print("SERIALIZER ERRORS:", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AddTravelRouteAPI(APIView):
#     def post(self,request,id):
#         print("######### Add Travel Route API #########ngr", request.data)
#         print("######### A---------------r", id)
#         TRAVELER=UserTable.objects.get(LOGIN_id=id)
#         serializer=AddTravelRouteSerializer(data=request.data)
#         if serializer.is_valid():
#             print("######### B---------------r")
#             serializer.save(TRAVELERID=TRAVELER)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VerifyRideBookingAPI(APIView):
#     def get(self, request, id): 
#         print("######### Verify Ride Booking API ######### User ID:", id) 
#         try:
#             # We filter by following the relationship: 
#             # Booking -> TravelRoute (TRAVELERID) -> User (TRAVELERID) -> Login (id)
#             booking = BookingTable.objects.filter(TRAVELERID__TRAVELERID__LOGIN_id=id)
            
#             if not booking.exists():
#                 print(f"No bookings found in database for User ID {id}")
#                 return Response({"error": "No booking found"}, status=status.HTTP_404_NOT_FOUND)
            
#             # Using the serializer that includes the ParcelImage field
#             serializer = BookingSerializer(booking, many=True)
            
#             print("Serialized data for Flutter: ", serializer.data)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             print("Error in Verify API:", str(e))
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class VerifyParcelBookingAPI(APIView):
#     def post(self,request,id):
#         guardian=BookingTable.objects.get(USERID=id)
#         serializer=BookingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(guardian=guardian)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class SendChatAPI(APIView):
#     def post(self, request):
#         sender_id = request.data['sender_id']
#         receiver_id = request.data['receiver_id']
        
#         try:
#             # Find User objects based on the Login ID sent from Flutter
#             c = UserTable.objects.get(LOGIN__id=sender_id)
#             d = UserTable.objects.get(LOGIN__id=receiver_id)
            
#             ChatTable.objects.create(
#                 sender=c,
#                 receiver=d,
#                 message=request.data['message']
#             )
#             return Response({"status": "success"}, status=200)
#         except UserTable.DoesNotExist:
#             return Response({"status": "error", "message": "User not found"}, status=404)

# from django.db.models import Q


# class ViewChatAPI(APIView):
#     def get(self, request, sender_id, receiver_id):
#         try:
#             sender_user = UserTable.objects.get(LOGIN__id=sender_id)
#             receiver_user = UserTable.objects.get(LOGIN__id=receiver_id)

#             chats = ChatTable.objects.filter(
#                 Q(sender=sender_user, receiver=receiver_user) |
#                 Q(sender=receiver_user, receiver=sender_user)
#             ).order_by('date')

#             serializer = ChatSerializer(chats, many=True)
#             return Response(serializer.data, status=200)

#         except UserTable.DoesNotExist:
#             return Response({"error": "One or both users do not exist."}, status=404)


# class ViewTraveller(APIView):
#     def get(self, request):
#         travelers = UserTable.objects.filter(LOGIN__UserType="traveler")
#         serializer = UserTableSerializer(travelers, many=True)
#         print("#########", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ViewUser(APIView):
#     def get(self, request):
#         travelers = UserTable.objects.filter(LOGIN__UserType="user")
#         serializer = UserTableSerializer(travelers, many=True)
#         print("#########", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class VerifyOtp(APIView):
#     def post(self, request, lid):
#         print("======", request.data)
#         booking_otp = request.data.get('otp')
#         booking_id = request.data.get('booking_id')
#         # try:
#         print("======", booking_id)
#         booking_obj = BookingTable.objects.get(id=booking_id)
#         print("===otpdata==-----------------=", booking_obj.OtpCode)
#         print("===type otp===", booking_otp)
#         if booking_obj.OtpCode == booking_otp:
#             booking_obj.BookingStatus = 'Verified'
#             booking_obj.save()
#             return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
#         # except BookingTable.DoesNotExist:
#         #     return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)    
    
# class reject_booking_api(APIView):
#     def post(self, request):
#         print("======", request.data)
#         booking_id = request.data.get('booking_id')
#         try:
#             booking_obj = BookingTable.objects.get(id=booking_id)
#             booking_obj.BookingStatus = 'Rejected'
#             booking_obj.save()
#             return Response({"message": "Booking rejected successfully"}, status=status.HTTP_200_OK)
#         except BookingTable.DoesNotExist:
#             return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)







# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import PaymentTable, BookingTable

# class CreatePaymentIntent(APIView):
#     def post(self, request):
#         print("######### Create Payment Intent API #########", request.data)
        
#         # 1. Extract data from request
#         data = request.data
#         booking_id = data.get('booking_id')
#         payment_method = data.get('payment_method')
#         amount = data.get('amount')

#         try:
#             # 2. Handle the Booking instance
#             # If booking_id is 0 or None, we set it to None (allowed by your model)
#             booking_instance = None
#             if booking_id and booking_id != 0:
#                 booking_instance = BookingTable.objects.get(id=booking_id)
#                 booking_instance.BookingStatus='paid'
#                 booking_instance.save()
#             # 3. Create and Save the Payment record
#             payment = PaymentTable.objects.create(
#                 BOOKINGID=booking_instance,
#                 TransactionType=payment_method,
#                 Amount=amount
#             )

#             return Response({
#                 "message": "Payment intent created successfully",
#                 "payment_id": payment.id
#             }, status=status.HTTP_201_CREATED)

#         except BookingTable.DoesNotExist:
#             return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class UpdateGratitudeAPI(APIView):
#     def post(self, request):
#         try:
#             booking_id = request.data.get("BOOKINGID")
#             tip_amount = request.data.get("GratitudeAmount")
#             print("---------", request.data)
#             booking = BookingTable.objects.get(id=booking_id)
#             booking.BookingStatus='received'
#             booking.save()
#             # Save tip
#             tip = TipTable.objects.create(
#                 BOOKING=booking,
#                 Tip=tip_amount
#             )

#             # Update booking status
#             booking.PaymentStatus = "Tip Sent"
#             booking.save()

#             return Response({
#                 "status": "success",
#                 "message": "Gratitude added successfully",
#                 "tip_id": tip.id
#             }, status=status.HTTP_200_OK)

#         except BookingTable.DoesNotExist:
#             return Response({
#                 "status": "error",
#                 "message": "Invalid Booking ID"
#             }, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             return Response({
#                 "status": "error",
#                 "message": str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.conf import settings
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.views import View
from .models import UserTable, PaymentTable
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from CordApp.models import *
from CordApp.serializer import *
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.views import View
from .models import UserTable, PaymentTable
# ==========================================
#              WEB ADMIN VIEWS
# ==========================================

class LoginPage(View):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            login_obj = LoginTable.objects.get(Username=username, Password=password)
            if login_obj.UserType == 'admin':
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
        return render(request, "viewcomplaint.html", {'val': complaints_obj})


class SendReply(View):
    def post(self, request, cid):
        complaints_obj = ComplaintsTable.objects.get(id=cid)
        complaints_obj.Reply = request.POST['reply']
        complaints_obj.save()
        return redirect('viewcomplaintpage')


class viewfeedbackpage(View):
    def get(self, request):
        feedback_obj = FeedbackTable.objects.all()
        return render(request, "viewfeedback.html", {'val': feedback_obj})


# class viewtrippage(View):
#     def get(self, request):
#         payment_obj = PaymentTable.objects.all()
#         return render(request, "viewtrip.html", {'val': payment_obj})




# # --- 1. VIEW PAYOUT CONSOLE ---
# class viewtrippage(View):
#     def get(self, request):
#         # Get all travelers
#         travelers = UserTable.objects.filter(LOGIN__UserType="traveler")
        
#         traveler_data = []
        
#         for t in travelers:
#             # Calculate Total Gross Earnings (Sum of 'Amount' in PaymentTable for this traveler)
#             # We filter bookings where the traveler matches
#             earnings = PaymentTable.objects.filter(
#                 BOOKINGID__TRAVELERID__TRAVELERID=t
#             ).aggregate(Sum('Amount'))['Amount__sum'] or 0.0
            
#             # Count total completed trips (Paid)
#             trips_count = PaymentTable.objects.filter(
#                 BOOKINGID__TRAVELERID__TRAVELERID=t
#             ).count()

#             traveler_data.append({
#                 'id': t.LOGIN.id, # We use LOGIN_id for identification
#                 'Name': t.Name,
#                 'PhoneNo': t.PhoneNo,
#                 'TotalTrips': trips_count,
#                 'TotalEarned': earnings
#             })

#         return render(request, "pay.html", {'travelers': traveler_data})

# class viewtrippage(View):
#     def get(self, request):
#         # --- Part 1: Individual Traveler Data (For the Table) ---
#         travelers = UserTable.objects.filter(LOGIN__UserType="traveler")
#         traveler_data = []
        
#         for t in travelers:
#             # Calculate Total Gross Earnings for this specific traveler
#             earnings = PaymentTable.objects.filter(
#                 BOOKINGID__TRAVELERID__TRAVELERID=t
#             ).aggregate(Sum('Amount'))['Amount__sum'] or 0.0
            
#             # Count total completed trips
#             trips_count = PaymentTable.objects.filter(
#                 BOOKINGID__TRAVELERID__TRAVELERID=t
#             ).count()

#             traveler_data.append({
#                 'id': t.LOGIN.id, 
#                 'Name': t.Name,
#                 'PhoneNo': t.PhoneNo,
#                 'TotalTrips': trips_count,
#                 'TotalEarned': earnings
#             })

#         # --- Part 2: Global Stats (For the Top Cards) ---
#         # Calculate the sum of ALL payments in the system
#         total_global_gross = PaymentTable.objects.aggregate(Sum('Amount'))['Amount__sum'] or 0.0

#         # Calculate the split
#         platform_revenue = total_global_gross * 0.05  # 5% for you
#         pending_payouts = total_global_gross * 0.95   # 95% for travelers

#         # --- Part 3: Send everything to the template ---
#         context = {
#             'travelers': traveler_data,
#             'platform_revenue': platform_revenue, # Variables for the stats deck
#             'pending_payouts': pending_payouts    # Variables for the stats deck
#         }

#         return render(request, "pay.html", context)

# In views.py

class viewtrippage(View):
    def get(self, request):
        travelers = UserTable.objects.filter(LOGIN__UserType="traveler")
        traveler_data = []
        
        # Global Counters
        total_system_gross = 0
        total_system_settled = 0
        
        for t in travelers:
            # 1. Calculate Gross Earnings (Total Income)
            gross = PaymentTable.objects.filter(
                BOOKINGID__TRAVELERID__TRAVELERID=t
            ).aggregate(Sum('Amount'))['Amount__sum'] or 0.0
            
            # 2. Calculate Total Settled (Already Paid Out)
            settled = SettlementTable.objects.filter(
                TRAVELER=t
            ).aggregate(Sum('Amount'))['Amount__sum'] or 0.0

            # 3. Calculations
            trips_count = PaymentTable.objects.filter(
                BOOKINGID__TRAVELERID__TRAVELERID=t
            ).count()
            
            # Logic: (Total Earned * 95%) - (Amount Already Sent)
            net_payable_balance = (gross * 0.95) - settled
            
            # Add to global totals for the top cards
            total_system_gross += gross
            total_system_settled += settled

            # Only show travelers who have earned money
            if gross > 0:
                traveler_data.append({
                    'id': t.LOGIN.id,
                    'Name': t.Name,
                    'PhoneNo': t.PhoneNo,
                    'TotalTrips': trips_count,
                    'TotalEarned': gross,
                    'NetPayable': net_payable_balance 
                })

        # --- Global Stats for Top Cards ---
        platform_revenue = total_system_gross * 0.05
        
        # Pending Payouts = (Total 95% Share) - (Total Already Paid)
        total_pending_payouts = (total_system_gross * 0.95) - total_system_settled

        context = {
            'travelers': traveler_data,
            'platform_revenue': platform_revenue,
            'pending_payouts': total_pending_payouts
        }

        return render(request, "pay.html", context)



# # --- 2. PROCESS SETTLEMENT (Form Submission) ---
# class SettlePayment(View):
#     def post(self, request):
#         traveler_id = request.POST.get('traveler_id') # This is the LOGIN_id
#         utr_number = request.POST.get('utr_number')
        
#         print(f"Processing Payout for Traveler ID: {traveler_id} | UTR: {utr_number}")
        
#         # Here you would typically save this "Payout" record to a new table (e.g., SettlementTable)
#         # For now, we will just reload the page to simulate success.
        
#         return HttpResponse('''<script>alert("Payout Recorded Successfully!");window.location="/viewtrippage";</script>'''),

# --- 2. PROCESS SETTLEMENT (Form Submission) ---
# In views.py
from django.utils import timezone
from .models import SettlementTable, UserTable # Make sure to import SettlementTable

class SettlePayment(View):
    def post(self, request):
        traveler_login_id = request.POST.get('traveler_id') 
        utr_number = request.POST.get('utr_number')
        
        # 1. Get the Traveler User Object
        traveler = UserTable.objects.get(LOGIN_id=traveler_login_id)
        
        # 2. Calculate the exact amount they are owed right now
        # (This prevents hacking the HTML input to send wrong amounts)
        
        # A. Total Gross Earnings
        gross_earnings = PaymentTable.objects.filter(
            BOOKINGID__TRAVELERID__TRAVELERID=traveler
        ).aggregate(Sum('Amount'))['Amount__sum'] or 0.0

        # B. Total Already Paid (Settlements)
        total_settled = SettlementTable.objects.filter(
            TRAVELER=traveler
        ).aggregate(Sum('Amount'))['Amount__sum'] or 0.0

        # C. Net Payable (95% of Gross - What we already sent)
        amount_to_pay = (gross_earnings * 0.95) - total_settled
        
        if amount_to_pay > 0:
            # 3. Create the Settlement Record
            SettlementTable.objects.create(
                TRAVELER=traveler,
                Amount=amount_to_pay,
                UTR=utr_number
            )
            print(f"Success: Paid ₹{amount_to_pay} to {traveler.Name}")
            return HttpResponse('''<script>alert("Settlement Successful!");window.location="/viewtrippage";</script>''')
        else:
            return HttpResponse('''<script>alert("Error: No pending balance to settle.");window.location="/viewtrippage";</script>''')


class adminhome(View):
    def get(self, request):
        admin_obj = TravelRouteTable.objects.all()
        return render(request, "admin_home.html", {'val': admin_obj})


# ==========================================
#               REST API VIEWS
# ==========================================

# --- Helper Function ---
def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP


class LoginAPI(APIView):
    def post(self, request):
        response_dict = {}
        username = request.data.get("username")
        password = request.data.get("Password")
        
        if not username or not password:
            response_dict["message"] = "Failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)
        
        t_user = LoginTable.objects.filter(Username=username, Password=password).first()
        
        if not t_user:
            response_dict["message"] = "Failed"
            return Response(response_dict, status=status.HTTP_404_NOT_FOUND)
        else:
            response_dict["message"] = "Success"
            response_dict["login_id"] = t_user.id
            response_dict["userrole"] = t_user.UserType
            return Response(response_dict, status=status.HTTP_200_OK)


class UserReg(APIView):
    def post(self, request):
        print("######### User Registration API #########", request.data)
        user_serial = UserSerializer(data=request.data)
        login_serial = LoginSerializer(data=request.data)

        if user_serial.is_valid() and login_serial.is_valid():
            login_profile = login_serial.save()
            user_profile = user_serial.save(LOGIN=login_profile)
            return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        
        print("User Errors:", user_serial.errors)
        print("Login Errors:", login_serial.errors)
        return Response(user_serial.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewRideTravelRouteAPI(APIView):
    def get(self, request):
        e = TravelRouteTable.objects.filter(RideType='Ride')
        serializer = TravelRouteSerializer(e, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewParcelTravelRouteAPI(APIView):
    def get(self, request):
        b = TravelRouteTable.objects.filter(RideType='Parcel')
        serializer = TravelRouteSerializer(b, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingAPI(APIView):
    def post(self, request):
        print("######### Booking API #########")
        trav_id = request.data.get('TRAVELERID')
        serializer = AddBookingSerializer(data=request.data)
        
        # 1. Fetch the User (Sender)
        try:
            user = UserTable.objects.get(LOGIN__id=request.data.get('USERID'))
            target_email = user.Email 
        except UserTable.DoesNotExist:
            return Response({"error": "Invalid USERID"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            otp = generate_otp()

            # 2. Save the Booking first
            booking = serializer.save(
                USERID=user,
                BookingStatus='Pending',
                OtpCode=otp
            )
            
            # 3. Determine Ride Type for Custom Email
            try:
                route_obj = TravelRouteTable.objects.get(id=trav_id)
                ride_type = route_obj.RideType # "Ride" or "Parcel"
                
                email_subject = 'Parcel Booking Confirmation & OTP'
                email_body = (
                    f'Hello {user.Name},\n\n'
                    f'Your parcel booking request has been received successfully.\n'
                    f'Booking ID: {booking.id}\n'
                    f'YOUR SECURE OTP: {otp}\n\n'
                    f'Please share this OTP with the traveler ONLY when they pick up your parcel.'
                )

                if ride_type == "Ride":
                    email_subject = 'Ride Booking Confirmation & OTP'
                    email_body = (
                        f'Hello {user.Name},\n\n'
                        f'Your ride has been successfully booked.\n'
                        f'Booking ID: {booking.id}\n'
                        f'YOUR SECURE OTP: {otp}\n\n'
                        f'Please share this OTP with the driver when you board the vehicle.'
                    )

                # 4. Send the Dynamic Email
                send_mail(
                    email_subject,
                    email_body,
                    'saanandsdb@gmail.com', # From Email
                    [target_email],         # To User (Sender)
                )

            except Exception as e:
                print(f"--- EMAIL FAILED: {e} ---")

            return Response({
                "message": "Booking created successfully",
                "booking_id": booking.id,
                "otp": otp
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewBookingHistoryAPI(APIView):    
    def get(self, request, lid):
        print("######### View Booking History API ######### lid:", lid)
        bookings = BookingTable.objects.filter(USERID__LOGIN_id=lid)
        serializer = BookingSerializer1(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NearestTravelersAPI(APIView):
    def get(self, request):
        a = UserTable.objects.all()
        serializer = UserSerializer(a, many=True)
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
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except BookingTable.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


class FeedbackReplyAPI(APIView):
    def get(self, request):
        d = FeedbackTable.objects.all()
        serializer = FeedbackSerializer(d, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewEarningsAPI(APIView):
    def get(self, request, lid):
        try:
            traveler = UserTable.objects.get(LOGIN_id=lid)
            
            # 1. Get ONLY the payments related to this traveler
            paid_transactions = PaymentTable.objects.filter(
                BOOKINGID__TRAVELERID__TRAVELERID=traveler
            )

            # 2. Total Earned: Sum of amounts from confirmed payments
            total_earned = paid_transactions.aggregate(Sum('Amount'))['Amount__sum'] or 0.0
            
            # 3. Total Kms: Sum Kms ONLY for routes that have a corresponding Payment
            total_kms = TravelRouteTable.objects.filter(
                TRAVELERID=traveler,
                bookingtable__paymenttable__isnull=False 
            ).distinct().aggregate(Sum('Kms'))['Kms__sum'] or 0.0
            
            # 4. Carbon Credits Logic: 3 Kms = 1 CC
            # We use integer division // to get whole credits
            carbon_credits = int(total_kms // 3)
            
            # 5. Recent Activity
            recent_payments = paid_transactions.order_by('-TransactionDate')[:10]
            
            history_data = []
            for p in recent_payments:
                route = p.BOOKINGID.TRAVELERID 
                
                # Individual CC earned for this specific trip (3km = 1CC)
                trip_kms = route.Kms or 0
                trip_cc = int(trip_kms // 3)

                history_data.append({
                    "id": f"TRN-{p.id}",
                    "type": route.RideType,
                    "amount": p.Amount,
                    "date": p.TransactionDate.strftime("%d-%m-%Y"),
                    "ccEarned": trip_cc
                })

            return Response({
                "total_kms": round(total_kms, 2),
                "total_earned": round(total_earned, 2),
                "carbon_credits": carbon_credits,
                "recent_activity": history_data
            }, status=status.HTTP_200_OK)

        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



class ViewFeedbackAPI(APIView):
    def get(self, request):
        i = FeedbackTable.objects.all()
        serializer = FeedbackSerializer(i, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendComplaintsAPI(APIView):
    def post(self, request, id):
        guardian = BookingTable.objects.get(USERID=id)
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(guardian=guardian)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendFeedbackAPI(APIView):
    def get(self, request, id):
        c = FeedbackTable.objects.filter(BOOKINGID__TRAVELERID__TRAVELERID__LOGIN_id=id)
        d = FeedbackSerializer(c, many=True)
        return Response(d.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        print("######### Add Feedback API #########", request.data)
        try:
            user_obj = UserTable.objects.get(LOGIN__id=id)
            booking_id = request.data.get('BOOKINGID')
            booking_obj = None
            if booking_id:
                booking_obj = BookingTable.objects.get(id=booking_id)

            serializer = SendFeedbackSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    USERID=user_obj,
                    BOOKINGID=booking_obj
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddTravelRouteAPI(APIView):
    def post(self, request, id):
        print("######### Add Travel Route API #########", request.data)
        try:
            TRAVELER = UserTable.objects.get(LOGIN_id=id)
            serializer = AddTravelRouteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(TRAVELERID=TRAVELER)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class VerifyRideBookingAPI(APIView):
    def get(self, request, id): 
        print("######### Verify Ride Booking API ######### User ID:", id) 
        try:
            # Check if user is PASSENGER or DRIVER
            booking = BookingTable.objects.filter(
                Q(USERID__LOGIN_id=id) | 
                Q(TRAVELERID__TRAVELERID__LOGIN_id=id)
            )

            if not booking.exists():
                print(f"--- User {id} has no bookings. Returning empty list. ---")
                # CHANGE IS HERE: Return 200 OK with data=[] instead of 404
                return Response([], status=status.HTTP_200_OK)
            
            serializer = BookingSerializer(booking, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error in Verify API:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyParcelBookingAPI(APIView):
    def post(self, request, id):
        try:
            guardian = BookingTable.objects.get(USERID=id)
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(guardian=guardian)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendChatAPI(APIView):
    def post(self, request):
        sender_id = request.data['sender_id']
        receiver_id = request.data['receiver_id']
        try:
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
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewUser(APIView):
    def get(self, request):
        users = UserTable.objects.filter(LOGIN__UserType="user")
        serializer = UserTableSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyOtp(APIView):
    def post(self, request, lid):
        print("======", request.data)
        booking_otp = request.data.get('otp')
        booking_id = request.data.get('booking_id')
        try:
            booking_obj = BookingTable.objects.get(id=booking_id)
            if booking_obj.OtpCode == booking_otp:
                booking_obj.BookingStatus = 'Verified'
                booking_obj.save()
                return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except BookingTable.DoesNotExist:
             return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


class reject_booking_api(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        try:
            booking_obj = BookingTable.objects.get(id=booking_id)
            booking_obj.BookingStatus = 'Rejected'
            booking_obj.save()
            return Response({"message": "Booking rejected successfully"}, status=status.HTTP_200_OK)
        except BookingTable.DoesNotExist:
            return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


class CreatePaymentIntent(APIView):
    def post(self, request):
        print("######### Create Payment Intent API #########", request.data)
        data = request.data
        booking_id = data.get('booking_id')
        payment_method = data.get('payment_method')
        amount = data.get('amount')

        try:
            booking_instance = None
            if booking_id and booking_id != 0:
                booking_instance = BookingTable.objects.get(id=booking_id)
                booking_instance.BookingStatus = 'paid'
                booking_instance.save()
            
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
            
            booking = BookingTable.objects.get(id=booking_id)
            booking.BookingStatus = 'received'
            booking.save()
            
            tip = TipTable.objects.create(
                BOOKING=booking,
                Tip=tip_amount
            )


            booking.PaymentStatus = "Tip Sent"
            booking.save()

            return Response({
                "status": "success",
                "message": "Gratitude added successfully",
                "tip_id": tip.id
            }, status=status.HTTP_200_OK)

        except BookingTable.DoesNotExist:
            return Response({"status": "error", "message": "Invalid Booking ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==========================================
#         MISSING API (ADDED FOR FIX)
# ==========================================

# ==========================================
#         PAYMENT & VERIFICATION APIs
# ==========================================

class UploadPaymentProofAPI(APIView):
    """
    Called by Flutter PaymentPage. 
    Updates the booking with UTR and Screenshot.
    """
    def post(self, request):
        print("######### Upload Payment Proof API #########", request.data)
        try:
            booking_id = request.data.get('booking_id')
            utr_number = request.data.get('utr_number')
            proof_file = request.FILES.get('payment_proof') 
            
            booking = BookingTable.objects.get(id=booking_id)
            
            # Save the new data to BookingTable
            booking.PaymentProof = proof_file
            booking.UTR = utr_number
            
            # Check if this is a tip or a regular payment
            if request.data.get('payment_method') == 'UPI_Screenshot_Gratitude':
                 booking.PaymentStatus = 'Tip Sent'
            else:
                 booking.PaymentStatus = 'Proof Uploaded'
                 
            booking.save()
            return Response({"message": "Proof uploaded successfully"}, status=status.HTTP_200_OK)
            
        except BookingTable.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ApprovePaymentAPI(APIView):
    """
    Handles payment verification from the Traveler side.
    Supports 'Paid' for approval and 'Payment Failed' for faulty screenshots.
    """
    def post(self, request):
        print("######### Approve Payment API #########", request.data)
        try:
            booking_id = request.data.get('booking_id')
            # 'status' will be either "Paid" or "Payment Failed" from Flutter
            new_status = request.data.get('status') 
            
            # 1. Fetch the booking instance
            booking = BookingTable.objects.get(id=booking_id)
            
            # 2. Update the status in BookingTable
            booking.PaymentStatus = new_status
            booking.save()
            
            # 3. Logic based on the status received
            if new_status == 'Paid':
                approved_amount = request.data.get('amount')
                # Generate and STORE the permanent record
                PaymentTable.objects.create(
                    BOOKINGID=booking,
                    TransactionType="UPI_VERIFIED",
                    Amount=float(approved_amount)
                )
                return Response({"message": "Payment Approved and Record Stored"}, status=status.HTTP_200_OK)
            
            elif new_status == 'Payment Failed':
                # No PaymentTable record created; user sees 'RETRY' button in Flutter
                return Response({"message": "Payment marked as Failed. User must retry."}, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid status received"}, status=status.HTTP_400_BAD_REQUEST)

        except BookingTable.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"CRITICAL ERROR in ApprovePaymentAPI: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)