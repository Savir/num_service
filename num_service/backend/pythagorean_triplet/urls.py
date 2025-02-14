from django.urls import path
from .views import TripletAPIView

urlpatterns = [
    path('', TripletAPIView.as_view(), name='pythagorean-triplet-api'),
]