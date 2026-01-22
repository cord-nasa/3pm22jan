
from django.urls import path

from CordApp.views import *



urlpatterns = [
    path('',LoginPage.as_view(), name='LoginPage'),
    path('viewuserpage',viewuserpage.as_view(), name='viewuserpage'),
    path('ApproveUser/<int:lid>',ApproveUser.as_view(), name='ApproveUser'),
    path('RejectUser/<int:lid>',RejectUser.as_view(), name='RejectUser'),
    path('viewbookingpage',viewbookingpage.as_view(),name='viewbookingpage'),
    path('viewcomplaintpage',viewcomplaintpage.as_view(),name='viewcomplaintpage'),
    path('SendReply/<int:cid>',SendReply.as_view(),name='SendReply'),
    path('viewfeedbackpage',viewfeedbackpage.as_view(),name='viewfeedbackpage'),
    path('viewtrippage',viewtrippage.as_view(),name='viewtrippage'),
    path('adminhome',adminhome.as_view(),name='adminhome'),

##################################USER API#######################################

    path('UserReg',UserReg.as_view(),name='userReg'),
    path('LoginAPI',LoginAPI.as_view(),name='LoginAPI'),
    path('ViewBookingHistoryAPI/<int:lid>',ViewBookingHistoryAPI.as_view(),name='ViewBookingHistoryAPI'),
    path('ViewParcelTravelRouteAPI',ViewParcelTravelRouteAPI.as_view(),name='ViewParcelTravelRouteAPI'),
    path('BookingAPI',BookingAPI.as_view(),name='BookingAPI'),
    path('ViewRideTravelRouteAPI',ViewRideTravelRouteAPI.as_view(),name='ViewRideTravelRouteAPI'),
    path('SendComplaintsAPI',SendComplaintsAPI.as_view(),name='SendComplaintsAPI'),
    path('ComplaintReplyAPI/<int:lid>',ComplaintReplyAPI.as_view(),name='ComplaintReplyAPI'),




    path('ViewFeedbackAPI',ViewFeedbackAPI.as_view(),name='ViewFeedbackAPI'),
    path('NearestTravelersAPI',NearestTravelersAPI.as_view(),name='NearestTravelersAPI'),
    path('FeedbackReplyAPI',FeedbackReplyAPI.as_view(),name='FeedbackReplyAPI'),
    path('ViewEarningsAPI/<int:lid>',ViewEarningsAPI.as_view(),name='ViewEarningsAPI'),
    # path('ParcelBookingAPI',ParcelBookingAPI.as_view(),name='ParcelBookingAPI'),
    path('SendFeedbackAPI/<int:id>',SendFeedbackAPI.as_view(),name='SendFeedbackAPI'),

    # ////////////////////////////////////// Traveler API //////////////////////////////////////

    # path('RideBookingAPI/<int:id>',RideBookingAPI.as_view(),name='RideBookingAPI'),
    path('VerifyRideBookingAPI/<int:id>',VerifyRideBookingAPI.as_view(),name='VerifyRideBookingAPI'),
    path('VerifyParcelBookingAPI/<int:id>',VerifyParcelBookingAPI.as_view(),name='VerifyParcelBookingAPI'),
    path('AddTravelRouteAPI/<int:id>',AddTravelRouteAPI.as_view(),name='AddTravelRouteAPI'), 
    path('chat/send/', SendChatAPI.as_view()),
    path('chat/view/<int:sender_id>/<int:receiver_id>/', ViewChatAPI.as_view()),
    path('ViewTraveller',ViewTraveller.as_view(),name='ViewTraveller'),
    path('ViewUser',ViewUser.as_view(),name='ViewUser'),
    path('VerifyOtp/<int:lid>',VerifyOtp.as_view(),name='VerifyOtp'),
    path('reject_booking_api',reject_booking_api.as_view(),name='reject_booking_api'),
    path('CreatePaymentIntent',CreatePaymentIntent.as_view(),name='CreatePaymentIntent'),
    path('addtipapi',UpdateGratitudeAPI.as_view(),name='AddTipApi'),
]
