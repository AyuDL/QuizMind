from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .services import consume_token
from .models import TokenPurpose
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer               #Keep on var to use it by DRF
    permission_classes = [permissions.AllowAny]

class ConfirmAccountView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token_value = request.data.get("token")
        user = consume_token(token_value, TokenPurpose.ACCOUNT_VALIDATION)

        if user is None:
            return Response({"detail": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"detail": "Compte confirmé."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token_value = request.data.get("token")
        password_value = request.data.get("password")

        user = consume_token(token_value, TokenPurpose.PASSWORD_RESET)

        if user is None:
            return Response({"detail": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password_value, user)
        except ValidationError as e:
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password_value)
        user.save()
        return Response({"detail": "Mot de passe réinitialisé."}, status=status.HTTP_200_OK)

class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserResetPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data["old_password"]
        password = serializer.validated_data["password"]

        if old_password == password:
            return Response({"detail": "Mot de passe identique."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(old_password):
            return Response({"detail": "Le mot de passe de votre compte n'est pas le bon. Réessayez."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(password)
        request.user.save()
        return Response({"detail" : "Mot de passe modifié."}, status=status.HTTP_200_OK)
