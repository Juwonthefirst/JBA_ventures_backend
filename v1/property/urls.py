from django.urls import path
from v1.property import views

urlpatterns = [
    path("", views.ListAndCreatePropertyView.as_view()),
    path("<int:pk>/", views.RetrieveOrUpdatePropertyView.as_view()),
    ]
