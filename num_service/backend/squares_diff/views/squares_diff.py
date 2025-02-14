from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from squares_diff.models import SquaresDiff  # Adjust import based on structure
from squares_diff.serializers import SquaresDiffSerializer


class SquaresDiffView(APIView):
    MAX_NUMBER = 100

    def get(self, request) -> Response:
        number = request.GET.get("number", None)
        try:
            number = int(number)
        except ValueError:
            return Response({"error": "Invalid number", "number": number}, status=status.HTTP_400_BAD_REQUEST)
        if not (0 <= number <= SquaresDiffView.MAX_NUMBER):
            return Response(
                {"error": f"Number must be between 0 and {SquaresDiffView.MAX_NUMBER}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        diff_request, _ = SquaresDiff.objects.get_or_create(number=number)
        diff_request.occurrences += 1

        # Serialize data (before calling .save, which will update "last_datetime")
        response_data = SquaresDiffSerializer(diff_request).data

        diff_request.save()  # .save will update the 'auto_now" last_datetime field

        return Response(response_data, status=status.HTTP_200_OK)
