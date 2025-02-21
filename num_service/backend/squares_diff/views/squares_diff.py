from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from squares_diff.models import SquaresDiff  # Adjust import based on structure
from squares_diff.serializers import SquaresDiffSerializer


class SquaresDiffAPIView(APIView):
    MAX_NUMBER = 100

    def get(self, request) -> Response:
        """Handles a GET request in the shape of http://localhost:8000/difference?number=10"""

        number = request.GET.get("number", None)
        if number is None:
            return Response({"error": "Expected 'number' as a query param"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            number = int(number)
        except ValueError:
            return Response({"error": "Invalid number", "number": number}, status=status.HTTP_400_BAD_REQUEST)

        if not (0 <= number <= SquaresDiffAPIView.MAX_NUMBER):
            # This validation is done here instead of at the model level (e.g., field validators)
            # because we want to enforce this limit specifically for the HTTP API. The model might
            # be used elsewhere without this restriction.
            return Response(
                {"error": f"Number must be between 0 and {SquaresDiffAPIView.MAX_NUMBER}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        squares_diff: SquaresDiff  # Just a type hint
        squares_diff, _ = SquaresDiff.objects.get_or_create(number=number)
        SquaresDiff.objects.filter(number=number).update(occurrences=F("occurrences") + 1)
        # In the query above, we could filter using .id rather than .number, but .number is clearer and it's indexed,
        # so should be equally performant
        squares_diff.refresh_from_db(fields=["occurrences"])

        # Serialize data (before calling .save, which will update "last_datetime")
        response_data = SquaresDiffSerializer(squares_diff).data

        squares_diff.save()  # .save will update the "auto_now" last_datetime field

        return Response(response_data, status=status.HTTP_200_OK)
