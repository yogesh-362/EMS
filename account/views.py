from django.shortcuts import render
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeRegistrationSerializer,EmployeeLoginSerializer,EmployeeProfileSerializer,EmployeeChangePasswordSerializer, UserPasswordResetSerializer, SendPasswordResetSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
import qrcode
from django.http import HttpResponse
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = EmployeeRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginView(APIView):
    def post(self, request, format=None):
        serializer = EmployeeLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(emp_email=email, password=password)
            print(email)
            print(password)
            print(user)
            if user:
                login(request, user)
                token = get_tokens_for_user(user)
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Email or password is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Email or password is not valid"}, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh Token Not Provided"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({"access": new_access_token}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Invalid Data"})

class EmployeeLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

            else:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logout(request)
                return Response({"message": "Logout Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class EmployeeProfileView(APIView):
    def get(self, request, format=None):
        try:
            serializer = EmployeeProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Anonymous User"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        try:
            user_profile = request.user
            serializer = EmployeeProfileSerializer(user_profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Anonymous User"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            request.user.delete()
            return Response({"message": "User Deleted Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "User is not Logged In"}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            serializer = EmployeeChangePasswordSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                return Response({'detail': "Password Updated Successfully"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Unexpected Error"}, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SendPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uid = serializer.validated_data.get('uid')
            token = serializer.validated_data.get('token')
            link = serializer.validated_data.get('link')
            return Response({"message": "Password Reset Link Is Been Send", "uid": uid, "token": token, "link": link})
        return Response({"message": "There was an unexpected error"})


class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': "Password Reset Successfully"})
        return Response(serializer.errors)


@api_view(['GET'])
def generate_qr_code(request):
    try:
        # Assuming you have only one employee for simplicity
        employee = Employee.objects.get(id=1)

        # Generate QR code data based on employee ID
        qr_code_data = f"employee_id:{employee.id}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response

    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def scan_qr_code(request):
    try:
        qr_code_data = request.data.get('qr_code_data')
        employee_id = int(qr_code_data.split(":")[1])

        employee = Employee.objects.get(id=employee_id)
        employee.status = not employee.status
        employee.save()

        return Response({"message": "Status updated successfully", "id": employee_id}, status=status.HTTP_200_OK)

    except (Employee.DoesNotExist, ValueError):
        return Response({"error": "Invalid QR code data or Employee not exist"}, status=status.HTTP_400_BAD_REQUEST)
