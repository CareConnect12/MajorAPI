from django.db import models
from django.contrib.auth.models import User

gen=(('Male','Male'),
     ('Female','Female'),
     ('Other','Other'))
sta=(('Andhra Pradesh','Andhra Pradesh'),
     ('Arunachal Pradesh','Arunachal Pradesh'),
     ('Assam','Assam'),
     ('Bihar','Bihar'),
     ('Chhattisgarh','Chhattisgarh'),
     ('Goa','Goa'),
     ('Gujarat','Gujarat'),
     ('Haryana','Haryana'),
     ('Himachal Pradesh','Himachal Pradesh'),
     ('Jharkhand','Jharkhand'),
     ('Karnataka','Karnataka'),
     ('Kerala','Kerala'),
     ('Madhya Pradesh','Madhya Pradesh'),
     ('Maharashtra','Maharashtra'),
     ('Manipur','Manipur'),
     ('Meghalaya','Meghalaya'),
     ('Mizoram','Mizoram'),
     ('Nagaland','Nagaland'),
     ('Odisha','Odisha'),
     ('Punjab','Punjab'),
     ('Rajasthan','Rajasthan'),
     ('Sikkim','Sikkim'),
     ('Tamil Nadu','Tamil Nadu'),
     ('Telangana','Telangana'),
     ('Tripura','Tripura'),
     ('Uttar Pradesh','Uttar Pradesh'),
     ('Uttarakhand','Uttarakhand'),
     ('West Bengal','West Bengal'),
     ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
     ('Chandigarh','Chandigarh'),
     (' Dadra and Nagar Haveli and Daman and Diu',' Dadra and Nagar Haveli and Daman and Diu'),
     ('Lakshadweep','Lakshadweep'),
     ('Delhi','Delhi'),
     ('Puducherry','Puducherry')
    )
status=(('Married','Married'),
        ('Unmarried','Unmarried'))
class registration(models.Model):
    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    full_name=models.CharField(max_length=200)
    fathers_name=models.CharField(max_length=200)
    gender=models.CharField(choices=gen,max_length=200)
    email=models.CharField(max_length=200,unique=True)
    code=models.TextField()
    address1=models.TextField()
    address2=models.TextField()
    city=models.CharField(max_length=50)
    state=models.CharField(choices=sta,max_length=50)
    zip=models.IntegerField()
    token=models.TextField(default='')
    is_verified=models.BooleanField(default=False)
    userRole=models.TextField(default="User")
    def __str__(self):
        return self.full_name

class feed(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    message=models.CharField(max_length=2000)
    def __str__(self):
        return self.name
class beds(models.Model):
    Hospital_name = models.CharField(max_length=300)
    Hospital_id=models.TextField()
    Bed_id=models.CharField(max_length=300,unique=True)
    Ward_number=models.CharField(max_length=100)
    Room_number=models.CharField(max_length=100)
    Bed_type=models.CharField(max_length=300)
    def __str__(self):
        return self.Bed_id

class hospitalinfo(models.Model):
    hospital_name=models.CharField(max_length=300)
    hospital_image=models.ImageField(upload_to="hospital_images")
    hospital_address=models.TextField()
    hospital_details=models.TextField()
    def __str__(self):
        return self.hospital_name
ge=(('Male','Male'),
     ('Female','Female'),
     ('Others','Others'))

class patient_info(models.Model):
    Hospital_name = models.CharField(max_length=300)
    Bed_id=models.CharField(max_length=300,unique=True)
    Ward_number=models.IntegerField()
    Room_number=models.IntegerField()
    Disease=models.CharField(max_length=200)
    Bed_type=models.CharField(max_length=300)
    patient_name=models.CharField(max_length=200)
    patient_gender=models.CharField(choices=ge,max_length=300)
    patient_age=models.PositiveBigIntegerField()
    address=models.TextField()
    mobile_number=models.PositiveBigIntegerField()
    current_medication=models.TextField()
    allergies=models.TextField()
    past_surgeries=models.TextField()
    insurance_policy=models.TextField()
    Policy_number=models.TextField()
    special_request=models.TextField()


class finalinformation(models.Model):
    Hospital_name = models.CharField(max_length=300)
    Bed_id=models.CharField(max_length=300,unique=True)
    Ward_number=models.IntegerField()
    Room_number=models.IntegerField()
    Disease=models.CharField(max_length=200)
    Bed_type=models.CharField(max_length=300)
    patient_name=models.CharField(max_length=200)
    patient_gender=models.CharField(choices=ge,max_length=300)
    patient_age=models.PositiveBigIntegerField()
    address=models.TextField()
    mobile_number=models.PositiveBigIntegerField()
    current_medication=models.TextField()
    allergies=models.TextField()
    past_surgeries=models.TextField()
    insurance_policy=models.TextField()
    Policy_number=models.TextField()
    special_request=models.TextField()



# Doctor Registration
class DoctorRegistration(models.Model):
    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    full_name=models.CharField(max_length=200)
    fathers_name=models.CharField(max_length=200)
    gender=models.CharField(choices=gen,max_length=200)
    email=models.CharField(max_length=200,unique=True)
    passcode=models.TextField()
    address1=models.TextField()
    address2=models.TextField()
    city=models.CharField(max_length=50)
    state=models.CharField(choices=sta,max_length=50)
    zip=models.IntegerField()
    Morning_slot=models.BooleanField(default=False)
    Evening_slot=models.BooleanField(default=False)
    Night_slot=models.BooleanField(default=False)
    Afternoon_slot=models.BooleanField(default=False)
    login_status=models.IntegerField(default=0)
    token=models.TextField(default='')
    is_verified=models.BooleanField(default=False)
    # license=models.FileField(upload_to="Doctor_licence")
    userRole=models.TextField(default="Doctor")
    def __str__(self):
        return self.full_name
    
    
# Doctor's appointment slot model
class Doctor_slot(models.Model):
    slot_hour=models.PositiveIntegerField(default=0)
    slot_type=models.CharField(max_length=200)
    slot_duration=models.TextField()
    def __str__(self):
        return self.slot_type

class Booked_slot(models.Model):
    appointment_date=models.DateField()
    booked_slot=models.TextField()
    Doctor_id=models.TextField()


class Appointment(models.Model):
    user_name = models.CharField(max_length=200)
    user_id=models.PositiveIntegerField()
    Doctor_id=models.PositiveIntegerField()
    doctor_name= models.CharField(max_length=200)
    booked_slot = models.CharField(max_length=50)
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')
    purpose = models.TextField()
    notes = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='Pending')
    status=models.CharField(max_length=200,default="Pending")
    is_virtual = models.BooleanField(default=True)
    meeting_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user_name} - {self.doctor_name}"


    