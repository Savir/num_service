from django.urls import path
from .views import SquaresDiffView

urlpatterns = [
    path('', SquaresDiffView.as_view(), name='difference-api'),
]