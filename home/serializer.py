from home.models import *
from rest_framework import serializers
import secrets


class registerserializer(serializers.ModelSerializer):
    class Meta:
        model = registration
        fields = "__all__"

    def create(self, validated_data):
        username = validated_data["email"]
        user = User.objects.filter(username=username)
        if user.exists():
            raise serializers.ValidationError({"error": "username is already taken"})
        user_token = secrets.token_hex(16)
        obj1 = registration.objects.create(
            full_name=validated_data["full_name"],
            fathers_name=validated_data["fathers_name"],
            gender=validated_data["gender"],
            email=validated_data["email"],
            code=validated_data["code"],
            address1=validated_data["address1"],
            address2=validated_data["address2"],
            city=validated_data["city"],
            state=validated_data["state"],
            zip=validated_data["zip"],
            token=user_token,
        )
        obj1.save()
        obj2 = User.objects.create(username=validated_data["email"], first_name="User")
        obj2.set_password(validated_data["code"])
        obj2.save()
        return user_token


class loginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class profileserializer(serializers.ModelSerializer):
    class Meta:
        model = registration
        fields = "__all__"


class feedbackserializer(serializers.ModelSerializer):
    class Meta:
        model = feed
        fields = "__all__"


class bedsserializer(serializers.ModelSerializer):
    class Meta:
        model = beds
        fields = "__all__"


class hospitalinfoserializer(serializers.ModelSerializer):
    class Meta:
        model = hospitalinfo
        fields = "__all__"

        def get_photo_url(self, obj):
            request = self.context.get("request")
            photo_url = obj.fingerprint.url
            return request.build_absolute_uri(photo_url)


class patientrequestserializer(serializers.ModelSerializer):
    class Meta:
        model = patient_info
        fields = "__all__"


class hospital(serializers.ModelSerializer):
    class Meta:
        model = hospitalinfo
        fields = "__all__"


class copyserializer(serializers.ModelSerializer):
    class Meta:
        model = beds
        fields = "__all__"


class finalinfoserializer(serializers.ModelSerializer):
    class Meta:
        model = finalinformation
        fields = "__all__"


class Doctorserializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegistration
        fields = "__all__"

    def create(self, validated_data):
        username = validated_data["email"]
        status_obj = User.objects.filter(username=username)
        user_token = secrets.token_hex(16)
        if status_obj.exists():
            raise serializers.ValidationError(
                {"error": "user with this username is already exists"}
            )
        obj1 = User.objects.create(username=username, first_name="Doctor")
        obj1.set_password(validated_data["passcode"])
        obj1.save()

        obj = DoctorRegistration.objects.create(
            full_name=validated_data["full_name"],
            fathers_name=validated_data["fathers_name"],
            gender=validated_data["gender"],
            email=username,
            passcode=validated_data["passcode"],
            address1=validated_data["address1"],
            address2=validated_data.get("address2", ""),
            city=validated_data["city"],
            state=validated_data["state"],
            zip=validated_data["zip"],
            Morning_slot=validated_data.get("Morning_slot", False),
            Evening_slot=validated_data.get("Evening_slot", False),
            Night_slot=validated_data.get("Night_slot", False),
            Afternoon_slot=validated_data.get("Afternoon_slot", False),
            token=user_token,
            contact_number=validated_data["contact_number"],
            Medical_license_number=validated_data["Medical_license_number"],
            Licence_issuing_authority=validated_data["Licence_issuing_authority"],
            Specialization=validated_data["Specialization"],
            Year_of_experience=validated_data["Year_of_experience"],
            Qualification=validated_data["Qualification"],
        )
        obj.save()
        return user_token


#  serializer for the Doctor's slot]
class Doctor_slot_serializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor_slot
        fields = "__all__"


# Serializer for booked appointment
class Bookedserializerget(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super(Bookedserializerget, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class Bookedserializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def create(self, validated_data):
        user_name = validated_data["user_name"]
        user_id = validated_data["user_id"]
        doctor_id = validated_data["Doctor_id"]
        doctor_name = validated_data["doctor_name"]
        booked_slot = validated_data["booked_slot"]
        appointment_date = validated_data["appointment_date"]
        purpose = validated_data["purpose"]
        notes = validated_data["notes"]
        obj = Appointment.objects.create(
            user_name=user_name,
            user_id=user_id,
            Doctor_id=doctor_id,
            doctor_name=doctor_name,
            booked_slot=booked_slot,
            appointment_date=appointment_date,
            purpose=purpose,
            notes=notes,
        )
        obj.save()

        Booked_slot_obj = Booked_slot.objects.create(
            appointment_id=obj.id,
            appointment_date=appointment_date,
            booked_slot=booked_slot,
            Doctor_id=doctor_id,
        )
        Booked_slot_obj.save()
        return validated_data


# Get Doctor's Serializer
class GetDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegistration
        fields = "__all__"


# Serilizer to insert the Beds data
class Insertbedsserializer(serializers.ModelSerializer):
    class Meta:
        model = beds
        fields = "__all__"

    def create(self, validated_data):
        username = self.context.get("username")  # Get username
        userId = self.context.get("userId")
        Bed_id = validated_data["Bed_id"]
        Ward_number = validated_data["Ward_number"]
        Room_number = validated_data["Room_number"]
        Bed_type = validated_data["Bed_type"]
        obj = beds.objects.create(
            Hospital_name=username,
            Hospital_id=userId,
            Bed_id=Bed_id,
            Ward_number=Ward_number,
            Room_number=Room_number,
            Bed_type=Bed_type,
        )
        obj.save()
        return validated_data


class Userserilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRegistration
        fields = "__all__"


# Serilaizer to insert the hospital
class HospitalDataserializer(serializers.ModelSerializer):
    class Meta:
        model = hospitalinfo
        fields = "__all__"

    def create(self, validated_data):
        username = validated_data["email"]
        password = validated_data["password"]
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            obj = hospitalinfo.objects.create(
                hospital_name=validated_data["hospital_name"],
                # hospital_image=validated_data['hospital_image'],
                hospital_address=validated_data["hospital_address"],
                hospital_details=validated_data["hospital_details"],
                phone_number=validated_data["phone_number"],
                website_url=validated_data["website_url"],
                email=validated_data["email"],
                city=validated_data["city"],
                state=validated_data["state"],
                zip_code=validated_data["zip_code"],
                registration_number=validated_data["registration_number"],
                hospital_type=validated_data["hospital_type"],
                specialties=validated_data["specialties"],
                password=validated_data["password"],
            )
            obj.save()
            user_data = User.objects.create(username=username)
            user_data.set_password(password)
            user_data.save()
            return validated_data
    
