from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils.datastructures import MultiValueDict
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from v1.authentication.serializers import LoginSerializer

User = get_user_model()
bad_request = status.HTTP_400_BAD_REQUEST
unauthorized = status.HTTP_401_UNAUTHORIZED


@api_view(["GET", "HEAD"])
def get_csrf(request):
    token = get_token(request)
    return Response({"csrf": token})


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=bad_request)

    email = serializer.validated_data.get("email")
    password = serializer.validated_data.get("password")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=unauthorized)

    if not user.check_password(password):
        return Response({"error": "Invalid email or password"}, status=unauthorized)
    refresh_token = RefreshToken.for_user(user)

    response = Response({"access": str(refresh_token.access_token)})
    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        secure=True,
        httponly=True,
        max_age=60 * 60 * 24 * 30,
        samesite="None",
    )
    return response


@api_view(["GET"])
def logout(request):
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return Response(
            {"error": "You don't have permission to use this view"}, status=unauthorized
        )
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        response = Response(status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie("refresh_token")
        return response

    except:
        return Response({"error": "invalid token"}, status=bad_request)


class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "You don't have permission to use this view"},
                status=unauthorized,
            )
        request._full_data = MultiValueDict({"refresh": [refresh_token]})
        try:
            response = super().post(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response({"error": "user doesn't exist"}, status=bad_request)

        if "refresh" in response.data:
            new_refresh_token = response.data.pop("refresh")
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                secure=True,
                httponly=True,
                max_age=60 * 60 * 24 * 30,
                samesite="None",
            )

        return response
