from django.urls import path
from .views import RegisterView, PreferredCategoriesView, CurrentUserView, ConfirmAccountView, ResetPasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("confirm-account/", ConfirmAccountView.as_view(), name='confirm_account'),
    path("password-reset/", ResetPasswordView.as_view(), name='password_reset'),
    path("me/", CurrentUserView.as_view(), name="me"),
    path("me/categories/", PreferredCategoriesView.as_view(), name="preferred-categories")
]
