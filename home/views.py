from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from home.models import *
from home.serializer import *
from home.models import *
from rest_framework import filters
from rest_framework.generics import ListAPIView
from home.login_update import update_login
from rest_framework import status
from .GenerateOtp import *
from rest_framework.response import Response
from rest_framework.views import APIView
import hashlib
import hmac
import time
import base64
import json



# Create your views here
class register(APIView):
    def post(self,request):
        serializer=registerserializer(data=request.data)
        if request.data['SourceSystem']:
            SourceSystem=request.data['SourceSystem']
        if not serializer.is_valid():
            return Response({'status':200,'message':serializer.errors})
        user_token=serializer.save()
        user=request.data['email']
        if(SourceSystem=="Mobile"):
            userOtp=GenerateOtp()
            MobileMail(userOtp,user)
            return Response({'status':200,'message':'verification token is sent',"Token":user_token,"Otp":userOtp})
        else:
            WebMail(user_token,user)
            return Response({'status':200,'message':'verification token is sent'})
            

@api_view(['GET'])
def verify_token_for_user(request):
     token=request.GET.get('token')
     user_obj=registration.objects.filter(token=token).update(is_verified=1)
     if user_obj==1:
          return Response({'status':status.HTTP_200_OK,'message':'verified'})
     else:
          return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid token'})

@api_view(['GET'])
def verify_token_for_Doctor(request):
     token=request.GET.get('token')
     user_obj=DoctorRegistration.objects.filter(token=token).update(is_verified=1)
     if user_obj==1:
          return Response({'status':status.HTTP_200_OK,'message':'verified'})
     else:
          return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid token'})


# Mobile token Verification
@api_view(['POST'])
def verify_token_Mobile(request):
        user_type=request.data['userType']
        token=request.data['token']
        if(user_type=="User"):
            user_obj=registration.objects.filter(token=token).update(is_verified=1)
        elif (user_type=="Doctor"):
            user_obj=DoctorRegistration.objects.filter(token=token).update(is_verified=1)
        if user_obj==1:
            return Response({'status':status.HTTP_200_OK,'message':'verified'})
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Invalid token'})
     

# for login user
class userlogin(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        obj_id=registration.objects.get(email=username)
        user_role=obj_id.userRole
        if obj_id:
            if obj_id.is_verified == True or obj_id.is_verified ==1:
                user=authenticate(username=username,password=str(password))
                if user is None:
                    return Response({'status':200,'message':'invlaid username and password'})
                request.session['username']=request.data['username']
                request.session['user_id']=obj_id.id
                request.session['user_role']=obj_id.userRole
                # request.session.set_expiry(30)
                print(request.session['username'])
                return Response({'status':status.HTTP_200_OK,'message':'success','Token':obj_id.token,'UserRole':obj_id.userRole,'user_id':obj_id.id,'username':obj_id.email})
            else:
                return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':" user is not verified"}) 
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'user not exist'})
    
# for profile
class profile(APIView):
    def get(self,request):
        if request.session.has_key('username'):
            user=request.session['username']
            obj=registration.objects.filter(email=user)
            serializer=profileserializer(obj,many=True)
            return Response({'status':200,'message':serializer.data})
        else:
            return Response({'status':200,'message':'login required'})
        
        
# for feedback
class feedback(APIView):
    def get(self,request):
        user=feed.objects.all()
        serializer=feedbackserializer(user,many=True)
        return Response({'status':200,'message':serializer.data})
    
    def post(self,request):
        serializer=feedbackserializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status':200,'message':'something went wrrong'})
        serializer.save()
        return Response({'status':200,'message':serializer.data})


# For requesting the bed
class requst_for_beds(APIView):
    def post(self,request):
        Bed_id=request.data['Bed_id']
        user=beds.objects.get(Bed_id=Bed_id)
        serializer=patientrequestserializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
        serializer.save()
        user.delete()
        return Response({'status':200,'message':'your request is sended to the hospital'})


# For filter the beds
class filterbeds(ListAPIView):
    queryset=beds.objects.all()
    serializer_class=bedsserializer
    filter_backends=[filters.SearchFilter]
    search_fields=['Hospital_name','Bed_id','Ward_number','Room_number','Bed_type']


# For View Hospital 
class viewhospital(ListAPIView):
    queryset=hospitalinfo.objects.all()
    serializer_class=hospitalinfoserializer
    filter_backends=[filters.SearchFilter]
    search_fields=['hospital_name','hospital_address','hospital_details']



# For view Request
class viewrequest(ListAPIView):
    queryset=patient_info.objects.all()
    serializer_class=patientrequestserializer
    filter_backends=[filters.SearchFilter]
    search_fields=['Hospital_name','Bed_id','Ward_number','Room_number','Disease','Bed_type','patient_name','patient_gender',
                   'patient_age','address','mobile_number','current_medication','allergies','past_surgeries','insurance_policy',
                   'Policy_number','special_request']



# For view get hospital by there id
@api_view(['get'])
def get_hospital_by_id(request,id):
    user=hospitalinfo.objects.filter(id=id,is_verified=True)
    serializer=hospitalinfoserializer(user,many=True)
    return Response({'status':200,'message':serializer.data})


# for View the beds based on the provided id
@api_view(['get'])
def view_beds(request,id):
    try:
        data=beds.objects.get(id=id)
        serializer=bedsserializer(data)
        return Response({'status':200,'message':serializer.data})
    except hospitalinfo.DoesNotExist:  
        return Response({'status':404,'message':'error'})
        
    

# For reject the request the patient request
@api_view(['get'])
def rejectrequest(request,id):
        user=patient_info.objects.filter(id=id)
        serializer=patientrequestserializer(user,many=True)
        for data in serializer.data:
              data_serializer=copyserializer(data=data)
              if data_serializer.is_valid():
                     data_serializer.save()
              else:
                     return Response({'status':200,'message':data_serializer.errors,'data':serializer.data})
        user.delete()
        return Response({'status':200,'message':'success','data':serializer.data})


# For Accept the request of the patient
@api_view(['get'])
def selectrequest(request,id):
        user=patient_info.objects.filter(id=id)
        serializer=patientrequestserializer(user,many=True)
        for data in serializer.data:
              data_serializer=finalinfoserializer(data=data)
              if data_serializer.is_valid():
                     data_serializer.save()
              else:
                     return Response({'status':200,'message':'somthing is wrong'})
        user.delete()
        return Response({'status':200,'message':'success'})



# For Dischsrge the patient
@api_view(['get'])
def discharge(request,id):
     user=finalinformation.objects.filter(id=id)
     serializer=finalinfoserializer(user,many=True)
     for data in serializer.data:
          data_serializer=copyserializer(data=data)
          if data_serializer.is_valid():
                data_serializer.save()
          else:
               return Response({'status':200,'message':'somthing is wrong'})
     user.delete()
     return Response({'status':200,'message':'success'})


# For Display the accepted patient's 
@api_view(['get'])
def finalinfo(request):
     user=finalinformation.objects.all()
     serializer=finalinfoserializer(user,many=True)
     return Response({'status':200,'message':serializer.data})

# Doctor's registration View
class Doctor_registration(APIView):
     def post(self,request):
        serializer=Doctorserializer(data=request.data)
        SourceSystem=request.data["SourceSystem"]
        if not serializer.is_valid():
            return Response({'status':404,'message':serializer.errors})
        user_token=serializer.save()
        user=request.data['email']
        if(SourceSystem=="Mobile"):
            userOtp=GenerateOtp()
            MobileMail(userOtp,user)
            return Response({'status':200,'message':'verification token is sent',"Token":user_token,"Otp":userOtp})
        else:
            MailTODoctor(user_token,user)
            return Response({'status':200,'message':'verification token is sent'})
        return Response({'status':status.HTTP_200_OK,'meesage':'verification token is sent'})


# For Doctor's Login
class Doctor_login(APIView):
     def post(self,request):
          passcode=request.data['passcode']
          username=request.data['username']
          obj=authenticate(username=username,password=passcode)
          if obj is None:
               return Response({'status':404,'message':"invalid credentials"})
          else:
               obj=DoctorRegistration.objects.get(email=username)
               request.session['username']=username
               request.session['user_id']=obj.id
               request.session['user_type']='Doctor'
               login_update_status=update_login(username,1)
               if (login_update_status=="successfull"): 
                    return Response({'status':200,'message':'login','username':request.session['username'],'Token':obj.token,'userRole':obj.userRole,'user_id':obj.id})



# List of the Doctor's 
@api_view(['GET'])
def GetAllDoctor(request):
    DoctorObj=DoctorRegistration.objects.filter(is_verified=True)
    serializer=GetDoctorSerializer(DoctorObj,many=True)
    return Response({'status':status.HTTP_200_OK,'Data':serializer.data})

# Data for the Doctor
@api_view(['POST'])
def GetDoctor(request):
    doctor_id=request.data['DoctorId']
    Doctorobj=DoctorRegistration.objects.filter(id=doctor_id)
    serializer=GetDoctorSerializer(Doctorobj,many=True)
    return Response({'status':status.HTTP_200_OK,'data':serializer.data})


# for Doctor_slot based on the Slot_type(morning , night.....)
class Doctor_slot_list_by_type(APIView):
     def post(self,request):
        slot_type=request.data['slot_type']
        obj=Doctor_slot.objects.filter(slot_type=slot_type)
        serializer=Doctor_slot_serializer(obj,many=True)
        return Response({'status':200,'message':serializer.data})

    
# Slot's For a Perticular Hospital
class Doctor_slot_find(APIView):
    def post(self,request):
        Doctor_id=request.data['DoctorId']
        Doctor_data=DoctorRegistration.objects.get(id=Doctor_id)
        request_data={}
        if(Doctor_data.Morning_slot==True):
            Morning_slot=Doctor_slot.objects.filter(slot_type="Morning")
            request_data["Morning"]=Doctor_slot_serializer(Morning_slot,many=True).data
        if (Doctor_data.Evening_slot==True):
            Evening_slot=Doctor_slot.objects.filter(slot_type="Evening")
            request_data["Evening"]=Doctor_slot_serializer(Evening_slot,many=True).data
        if (Doctor_data.Night_slot==True):
            Night_slot=Doctor_slot.objects.filter(slot_type="Night")
            request_data["Night"]=Doctor_slot_serializer(Night_slot,many=True).data
        if (Doctor_data.Afternoon_slot==True):
            Afternoon_slot=Doctor_slot.objects.filter(slot_type="Afternoon")
            request_data["Afternoon"]=Doctor_slot_serializer(Afternoon_slot,many=True).data
        return Response({'status':status.HTTP_200_OK,'MorningSlot':request_data})
        

# For dispaly the Booked slot's
class Bookedslot(APIView):
     def post(self,request):
            obj=Appointment.objects.all()
            serializer=Bookedserializer(obj,many=True)
            return Response({'status':200,'message':serializer.data})
     
    
# For Display the Available slot
# class Available_slot(APIView):
#      def post(self,request):
#           slot=request.data['slot']
#           slot_date=request.data['slot_date']
#           try:
#             obj=booking_status.objects.filter(booked_slot=slot,appointment_date=slot_date)
#             booked_appoint=obj.values_list('booked_slot',flat=True)
#             available_slots=Doctor_slot.objects.exclude(slot_duration__in=booked_appoint)
#             serializer=Doctor_slot_serializer(available_slots,many=True)
#             return Response({'status':200,'message':serializer.data})
#           except Appointment.DoesNotExist:
#             obj1=Doctor_slot.objects.all()
#             serializer=Doctor_slot_serializer(obj1,many=True)
#             return Response({'status':status.HTTP_200_OK,'message':serializer.data})

    

    
class Available_slot_For_Doctor(APIView):
    def post(self,request):
        slot_date=request.data['slot_date']
        Doctor_id=request.data['Doctor_id']
        try:
            Doctor_data=DoctorRegistration.objects.get(id=Doctor_id)
            booked_slot=Booked_slot.objects.filter(appointment_date=slot_date,Doctor_id=Doctor_id)
            booked_slot_by_date=booked_slot.values_list('booked_slot',flat=True)
            Available_slot=Doctor_slot.objects.exclude(slot_duration__in=booked_slot_by_date)
            final_result={}
            if Doctor_data.Morning_slot:
                final_result['Morning'] = Doctor_slot_serializer(Available_slot.filter(slot_type="Morning"), many=True).data
            if Doctor_data.Night_slot:
                final_result['Night'] = Doctor_slot_serializer(Available_slot.filter(slot_type="Night"), many=True).data
            if Doctor_data.Afternoon_slot:
                final_result['Afternoon'] = Doctor_slot_serializer(Available_slot.filter(slot_type="Afternoon"), many=True).data
            if Doctor_data.Evening_slot:
                final_result['Evening'] = Doctor_slot_serializer(Available_slot.filter(slot_type="Evening"), many=True).data
            # serializer=Doctor_slot_serializer(Available_slot,many=True)
            return Response({'status':status.HTTP_200_OK,'data':final_result})
        except DoctorRegistration.DoesNotExist:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Doctor not exist'})
        

class requestforappointment(APIView):
     def post(self,request):
          if request.session.has_key('username') and request.session.has_key('user_id'):
               user_name=request.session['username']
               user_id=request.session['user_id']
               data = request.data.copy()
               data['username'] = user_name
               data['userId'] = user_id
               serializer=Bookedserializer(data=data)
               if not serializer.is_valid():
                    return Response({'status':status.HTTP_400_BAD_REQUEST,'error':serializer.errors})
               serializer.save()
               return Response({'status':status.HTTP_200_OK,'message':'success'})
            
class requestforappointmentMobile(APIView):
     def post(self,request):
               serializer=Bookedserializer(data=request.data)
               if not serializer.is_valid():
                    return Response({'status':status.HTTP_400_BAD_REQUEST,'error':serializer.errors})
               serializer.save()
               return Response({'status':status.HTTP_200_OK,'message':'success'})

       
# for display the appointment status to the user as well as doctor's
class appointment_status(APIView):
     def get(self,request): 
        if request.session.has_key('user_id') and  request.session.has_key('user_type'):
                user_type=request.session['user_type']  
                user_id=request.session['user_id']
                if user_type=='User':
                    obj_user=Appointment.objects.filter(user_id=user_id)
                    serializer_user=Bookedserializer(obj_user,many=True,fields=['user_name','doctor_name','booked_slot','appointment_date','status','payment_status'])
                    return Response({'status':status.HTTP_200_OK,'message':serializer_user.data})
                elif user_type=='Doctor':
                     obj_doctor=Appointment.objects.filter(Doctor_id=user_id)
                     serializer_doctor=Bookedserializer(obj_doctor,many=True,fields=['user_name','booked_slot','appointment_date','purpose','notes','status','payment_status'])
                     return Response({'status':status.HTTP_200_OK,'message':serializer_doctor.data}) 
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'error':'login required'})
        

class appointment_status_mobile(APIView):
     def post(self,request): 
                user_type=request.data['userRole']  
                user_id=request.data['userId']
                if user_type=='User':
                    obj_user=Appointment.objects.filter(user_id=user_id)
                    serializer_user=Bookedserializerget(obj_user,many=True,fields=['id','user_name','doctor_name','booked_slot','appointment_date','status','payment_status'])
                    return Response({'status':status.HTTP_200_OK,'message':serializer_user.data})
                elif user_type=='Doctor':
                     obj_doctor=Appointment.objects.filter(Doctor_id=user_id)
                     serializer_doctor=Bookedserializerget(obj_doctor,many=True,fields=['id','user_name','booked_slot','appointment_date','purpose','notes','status','payment_status'])
                     return Response({'status':status.HTTP_200_OK,'message':serializer_doctor.data}) 


class logout_user(APIView):
     def post(self,request):
          if request.session.has_key('user_id'):
               request.session.set_expiry(1)
               return Response({'status':status.HTTP_200_OK,'message':'logout'})
          else:
               return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'no user login'})

# Service For the Profile data For the Mobile APP
class profile_data(APIView):
     def post(self,request):
          user_role=request.data['userRole']
          token=request.data['token']   
          if(user_role=="User"):
            obj=registration.objects.filter(token=token)
            serializer=profileserializer(obj,many=True)
          elif(user_role=="Doctor"):
            obj=DoctorRegistration.objects.filter(token=token)
            serializer=DoctorProfileSerializer(obj,many=True) 
          else:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'please provide the User Role'})         
          return Response({'status':status.HTTP_200_OK,'message':serializer.data})
        
     
# Service To Find the all bed's for the Perticular Hospital
class ViewAllBedInHospital(APIView):
    def post(self,request):
        HospitalId=request.data['HospitalId']
        BedObj=beds.objects.filter(Hospital_id=HospitalId)
        serilaizer=bedsserializer(BedObj,many=True)
        return Response({'status':status.HTTP_200_OK,'Data':serilaizer.data})

    
# Service For Insert the Bed's Data 
class BedsService(APIView):
    def post(self,request):
        if request.session.has_key("username"):
            serializer = Insertbedsserializer(data=request.data, context={
            'username': request.session['username'],
            'userId': request.session['userId']
             })
            if not serializer.is_valid():
                return Response({'status':status.HTTP_400_BAD_REQUEST,'error':serializer.errors})
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'success'})
        else:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Hospital is not logged in'})


class GenerateMeetingLink(APIView):
    def post(self, request):
        Appitment_id=request.data['AppointmentId']
        app_id = 1825238297
        server_secret = "005d82e1cc382fa4d02da21d2d8d894f"
        room_id = str(int(time.time()))  # Unique Room ID based on timestamp
        user_id = str(int(time.time()))  # Unique User ID

        # Generate Zego Token
        payload = {
            "app_id": app_id,
            "room_id": room_id,
            "user_id": user_id,
            "privilege": {"1": 1, "2": 1},
            "expire_time": int(time.time()) + 3600,  # Token valid for 1 hour
        }
        payload_str = json.dumps(payload, separators=(",", ":"))
        digest = hmac.new(server_secret.encode(), payload_str.encode(), hashlib.sha256).digest()
        token = base64.b64encode(digest + payload_str.encode()).decode()
        # Generate Meeting Link
        meeting_link = f"https://video-conference-zpob.onrender.com/video_call/?roomID={room_id}"
        AppointmentData=Appointment.objects.get(id=Appitment_id)
        AppointmentData.meeting_link=meeting_link
        AppointmentData.status="Approve"
        AppointmentData.save()
        MeetingLinkMail(meeting_link,AppointmentData.user_name)
        # MeetingLinkMail(meeting_link,Doctor_email)
        return Response({"meeting_link": meeting_link})


# Service for the Regenerate the otp for mobile
class GeneratenewOtpMobile(APIView):
    def post(self,request):
        email_user=request.data['userEmail']
        userobj=User.objects.get(username=email_user)
        if userobj:
            if(userobj.first_name=="User"):
                userregister=registration.objects.get(email=email_user)
                usertoken=registerserializer(userregister)
            elif(userobj.first_name=="Doctor"):
                userregister=DoctorRegistration.objects.get(email=email_user)
                usertoken=Doctorserializer(userregister)
            otp=GenerateOtp()
            MobileMail(otp,email_user)
            return Response({'status':status.HTTP_200_OK,'Token':usertoken.data['token'],'Otp':otp})
        else:
            return Response({'status':HTTP_200_OK,'message':'Invalid email User not Exists'})
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':"Something is wrong"})

class Rejectappointment(APIView):
    def post(self,request):
        Appoitment_id=request.data['AppointmentId']
        obj=Appointment.objects.get(id=Appoitment_id)
        obj.status="Reject"
        obj.save()
        obj1=Booked_slot.objects.get(appointment_id=Appoitment_id)
        obj1.delete()
        return Response({'status':status.HTTP_200_OK,'message':'appointment rejected'})  


class AddHospital(APIView):
    def post(self,request):
        serializer=HospitalDataserializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'error':serializer.errors})
        serializer.save()
        return Response({'status':status.HTTP_200_OK,'message':"success"})     
    
# hospital_login
class hospital_login(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user_obj=authenticate(username=username,password=password)
        if user_obj is None:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'error':'Invalid username or password'})
        else:
            user_data=hospitalinfo.objects.get(email=username)
            request.session['username']=username
            request.session['userRole']="Hospital"
            request.session['userId']=user_data.id
            return Response({'status':status.HTTP_200_OK,'message':request.session['username']})



        


