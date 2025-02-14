from django.urls import path
from .views import SquaresDiffAPIView

urlpatterns = [
    path('', SquaresDiffAPIView.as_view(), name='squares-diff-api'),
]