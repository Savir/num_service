from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pythagorean_triplet.models import PythagoreanTriplet
from pythagorean_triplet.serializers import PythagoreanTripletSerializer


class TripletAPIView(APIView):
    """API to check if (a, b, c) is a Pythagorean triplet and return its product."""

    def get(self, request) -> Response:
        """Handles GET requests."""
        number = request.GET.get("number", None)
        if number is None:
            return Response(
                {"error": "You must provide a 'number' as a query param"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            number = int(number)
        except ValueError:
            return Response({"error": "Invalid number", "number": number}, status=status.HTTP_400_BAD_REQUEST)

        pythagorean_triplet: PythagoreanTriplet
        pythagorean_triplet, _ = PythagoreanTriplet.objects.get_or_create(number=number)
        pythagorean_triplet.occurrences += 1

        serializer = PythagoreanTripletSerializer(pythagorean_triplet)
        pythagorean_triplet.save()  # This will update the models' last_datetime attribute
        # TODO: If we don't find a triplet for the provided input... should we return a 404?
        #       Probably not, because the endpoint exists and it worked fine, and the calculations worked
        #       and all that. But this could lead to an interesting (and potentially heated) debate
        return Response(serializer.data, status=status.HTTP_200_OK)
