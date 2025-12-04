from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  *


urlpatterns = [
    path('token', TokenObtainPairView.as_view(),name='token_obtain'),
]
