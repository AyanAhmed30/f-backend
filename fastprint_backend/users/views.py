import jwt
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UserSerializer,  # Serializer for admin user listing
)
from .tokens import email_verification_token
from .utils import send_verification_email, send_password_reset_email

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uidb64 = urlsafe_base64_encode(smart_bytes(user.pk))
            token = email_verification_token.make_token(user)
            send_verification_email(user, uidb64, token)
            return Response(
                {"message": "Registered successfully. Please check your email to verify your account."},
                status=status.HTTP_201_CREATED,
            )
        else:
            logger.error(f"Registration errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            return Response({"message": "Email already verified."}, status=status.HTTP_200_OK)

        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            # Skip verification check for admin users
            if not user.is_verified and not user.is_admin:
                return Response({"error": "Email not verified."}, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "is_admin": user.is_admin,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.pk))
                token = PasswordResetTokenGenerator().make_token(user)
                send_password_reset_email(user, uidb64, token)
            except User.DoesNotExist:
                # Avoid user enumeration
                pass
            return Response(
                {"message": "If that email exists, a reset link has been sent."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if PasswordResetTokenGenerator().check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data["password"])
                user.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


# === Admin Views ===

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            users = User.objects.all().order_by("-created_at")
            serializer = UserSerializer(users, many=True)
            return Response(
                {"status": "success", "results": len(serializer.data), "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error("Failed to fetch users", exc_info=True)
            return Response(
                {"status": "error", "message": "Failed to fetch users."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminUserDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"status": "error", "message": "You cannot delete yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(
                {"status": "success", "message": "User deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error("Error deleting user", exc_info=True)
            return Response(
                {"status": "error", "message": "An error occurred while deleting the user."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
