from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pythagorean_triplet.models import PythagoreanTriplet
from pythagorean_triplet.serializers import PythagoreanTripletSerializer


class TripletAPIView(APIView):
    """API to check if (a, b, c) is a Pythagorean triplet and return its product."""

    MAX_NUMBER = 1_000_000_000

    def get(self, request) -> Response:
        """Handles GET requests."""
        number = request.GET.get("number", None)
        try:
            number = int(number)
        except ValueError:
            return Response({"error": "Invalid number", "number": number}, status=status.HTTP_400_BAD_REQUEST)
        if not (0 <= number <= TripletAPIView.MAX_NUMBER):
            return Response(
                {"error": f"Number must be between 0 and {TripletAPIView.MAX_NUMBER}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        triplet, _ = PythagoreanTriplet.objects.get_or_create(number=number)
        triplet.occurrences += 1

        serializer = PythagoreanTripletSerializer(triplet)
        triplet.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
