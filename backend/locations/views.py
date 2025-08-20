from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer


class LocationList(APIView):
    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        count_size = 10
        start = (page - 1) * count_size
        end = start + count_size

        all_locations = Location.objects.all()
        serializer = LocationSerializer(
            all_locations[start:end],
            many=True,
        )
        return Response(serializer.data)
