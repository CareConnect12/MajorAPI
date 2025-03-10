import random
from django.core.mail import send_mail
from django.conf import settings


def GenerateOtp():
        otp=str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
        return otp


# Send Verification mail For the Website along with the token
def WebMail(user_token,user):
        subject="Account Verification for CareConnect"
        message = (
        f"Dear User,\n\n"
        f"Thank you for registering with CareConnect.\n\n"
        f"To complete the registration process and ensure the security of your account, "
        f"please verify your email address by clicking the link below:\n"
        f"https://minor-api-new.onrender.com/login/?token={user_token}\n\n"
        f"If you are unable to click the link above, please copy and paste it into your web browser's address bar.\n\n"
        f"Once your email address has been verified, you will gain full access to our platform and its features.\n\n"
        f"If you did not register with CareConnect, please ignore this email.\n\n"
        f"Thank you for choosing CareConnect. If you have any questions or need further assistance, "
        f"please contact us at CareConnect.support@gmail.com.\n\n"
        f"Best regards,\n"
        f"CareConnect Team"
        )
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[user]
        send_mail(subject,message,from_email,recipient_list)

    
# Send Mail for the Mobile along with the otp
def MobileMail(user_otp,user):
        subject="Account Verification for CareConnect"
        message = (
        f"Dear User,\n\n"
        f"Thank you for registering with CareConnect.\n\n"
        f"To complete the registration process and ensure the security of your account, "
        f"please verify your email address using the One-Time Password (OTP) provided below:\n\n"
        f"Your OTP: {user_otp}\n\n"
        f"Please enter this OTP in the verification section of the CareConnect platform.\n\n"
        f"If you did not request this, please ignore this email.\n\n"
        f"Thank you for choosing CareConnect. If you have any questions or need further assistance, "
        f"please contact us at CareConnect.support@gmail.com.\n\n"
        f"Best regards,\n"
        f"CareConnect Team"
        )
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[user]
        send_mail(subject,message,from_email,recipient_list)

def MeetingLinkMail(meeting_link,user):
        subject="Account Verification for CareConnect"
        message = (
        f"Dear User,\n\n"
        f"Thank you for registering with CareConnect.\n\n"
        f"To complete the registration process and ensure the security of your account, "
        f"please verify your email address by clicking the link below:\n"
        f"{meeting_link}\n\n"
        f"If you are unable to click the link above, please copy and paste it into your web browser's address bar.\n\n"
        f"Once your email address has been verified, you will gain full access to our platform and its features.\n\n"
        f"If you did not register with CareConnect, please ignore this email.\n\n"
        f"Thank you for choosing CareConnect. If you have any questions or need further assistance, "
        f"please contact us at CareConnect.support@gmail.com.\n\n"
        f"Best regards,\n"
        f"CareConnect Team"
        )
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[user]
        send_mail(subject,message,from_email,recipient_list)

def MailTODoctor():
        subject="Account Verification for CareConnect"
        message = (
        f"Dear User,\n\n"
        f"Thank you for registering with CareConnect.\n\n"
        f"To complete the registration process and ensure the security of your account, "
        f"please verify your email address by clicking the link below:\n"
        f"https://minor-api-new.onrender.com/DoctorLogin/?token={user_token}\n\n"
        f"If you are unable to click the link above, please copy and paste it into your web browser's address bar.\n\n"
        f"Once your email address has been verified, you will gain full access to our platform and its features.\n\n"
        f"If you did not register with CareConnect, please ignore this email.\n\n"
        f"Thank you for choosing CareConnect. If you have any questions or need further assistance, "
        f"please contact us at CareConnect.support@gmail.com.\n\n"
        f"Best regards,\n"
        f"CareConnect Team"
        )
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[user]
        send_mail(subject,message,from_email,recipient_list)