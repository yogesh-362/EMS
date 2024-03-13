from rest_framework.serializers import ModelSerializer
from .models import Employee
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeRegistrationSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)


class EmployeeLoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Employee
        fields = ['email', 'password']


class EmployeeProfileSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeChangePasswordSerializer(ModelSerializer):
    password = serializers.CharField(max_length=50, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=50, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Employee
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Password2 Doesn't Matched")
        user.set_password(password)
        user.save()
        return super().validate(data)

class SendPasswordResetSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Employee
        fields = ['email']

    def validate(self, data):
        email = data.get("email")
        if Employee.objects.filter(emp_email=email).exists():
            employee = Employee.objects.get(emp_email=email)
            uid = urlsafe_base64_encode(force_bytes(employee.id))
            token = PasswordResetTokenGenerator().make_token(employee)
            link = "http://127.0.0.1:8000/user/reset/" + uid + "/" + token

            data['uid'] = uid
            data['token'] = token
            data['link'] = link
            body = 'Click Following Link to Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': employee.emp_email
            }
            Util.send_mail(data)
        else:
            raise ValueError("You Are Not Registered")
        data['uid'] = uid
        data['token'] = token
        data['link'] = link
        return data


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input-type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input-type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password Doesn't Match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = Employee.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not valid or expired")

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not valid or expired")


from rest_framework import serializers
import qrcode
from io import BytesIO
from django.core.files import File


class CheckInOutSerializer(serializers.Serializer):
    action = serializers.BooleanField()

    def generate_qr_code(self, action):
        action_str = "in" if action else "out"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(action_str)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        filename = f"qrcode-{action_str}.png"
        file_buffer = File(buffer, name=filename)
        return file_buffer

    def save(self):
        action = self.validated_data['action']
        return self.generate_qr_code(action)
