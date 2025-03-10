from django.contrib import admin
from django.urls import path,include
from home.models import *
from home.views import *

urlpatterns = [
    path('register/',register.as_view()),
    path('login_user/',userlogin.as_view()),
    path('profile/',profile.as_view()),
    path('feedback/',feedback.as_view()),
    path('viewbeds/',filterbeds.as_view()),
    path('view_beds/<id>/',view_beds),
    path('viewhospital/',viewhospital.as_view()),
    path('viewrequest/',viewrequest.as_view()),
    path('get_hospital_by_id/<id>/',get_hospital_by_id),
    path('reject/<id>/',rejectrequest),
    path('select/<id>/',selectrequest),
    path('request_for_beds/',requst_for_beds.as_view()),
    path('discharge/<id>/',discharge),
    path('viewpatient/',finalinfo),
    path('admin/', admin.site.urls),
    path('doctorregisteration/',Doctor_registration.as_view()),
    path('Doctor_login/',Doctor_login.as_view()),
    path('Doctorlist/',GetAllDoctor),
    path('Doctor_slot/',Doctor_slot_list_by_type.as_view()),
    path('booked_slot/',Bookedslot.as_view()),
    # path('Available_slot/',Available_slot.as_view()),
    path('Available_slot_For_Doctor/',Available_slot_For_Doctor.as_view()),
    path('requestforappointment/',requestforappointment.as_view()),
    path('appointment_status/',appointment_status.as_view()),
    path('login/',verify_token_for_user),
    path('DoctorLogin/',verify_token_for_Doctor),   
    path('logout/',logout_user.as_view()),
    path('profile_data/',profile_data.as_view()),
    path('Doctor_slot_find/',Doctor_slot_find.as_view()),
    path('viewBedByHospital/',ViewAllBedInHospital.as_view()),
    path('createrbed/',BedsService.as_view()),
    path('generatelink/',GenerateMeetingLink.as_view()),
    path('verify_token_Mobile/',verify_token_Mobile),
    path('GeneratenewOtpMobile/',GeneratenewOtpMobile.as_view()),
    path('Rejectappointment/',Rejectappointment.as_view()),
    path('GetDoctor/',GetDoctor),
    path('requestforappointmentMobile/',requestforappointmentMobile.as_view())
]