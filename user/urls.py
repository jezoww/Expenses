from django.urls import path

from user.views import RegisterAPIView, RegisterCheckAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('register/check', RegisterCheckAPIView.as_view()),
]