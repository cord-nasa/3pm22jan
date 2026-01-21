from django.contrib import admin

from CordApp.models import *

# Register your models here.

admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(BookingTable)
admin.site.register(ComplaintsTable)
admin.site.register(FeedbackTable)
admin.site.register(PaymentTable)
admin.site.register(TravelRouteTable)
admin.site.register(ChatTable)
admin.site.register(TipTable)

