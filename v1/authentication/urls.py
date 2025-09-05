from django.urls import path
from v1.authentication import views

urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("token/refresh/", views.TokenRefreshView.as_view()),
    path("csrf/", views.get_csrf),
]
