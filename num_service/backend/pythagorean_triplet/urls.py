from django.urls import path

from .views import PythagoreanTripletAPIView

urlpatterns = [
    path('', PythagoreanTripletAPIView.as_view(), name='pythagorean-triplet-api'),
]