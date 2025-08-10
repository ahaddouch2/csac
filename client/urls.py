# urls.py
from django.urls import path
from .views import GetTokenView

urlpatterns = [
    path('api/get_tokens/<str:email>', GetTokenView.as_view(), name='get_token'),
]
