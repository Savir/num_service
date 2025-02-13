from django.urls import path
from .views import DiffRequestView

urlpatterns = [
    path('', DiffRequestView.as_view(), name='difference-api'),
]