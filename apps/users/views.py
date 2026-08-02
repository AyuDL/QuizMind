from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import consume_token
from .models import TokenPurpose
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer               #Keep on var to use it by DRF
    permission_classes = [permissions.AllowAny]

class ConfirmAccountVIew(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token_value = request.data.get("token")
        user = consume_token(token_value, TokenPurpose.ACCOUNT_VALIDATION)

        if user is None:
            return Response({"detail": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"detail": "Compte confirmé."}, status=status.HTTP_200_OK)