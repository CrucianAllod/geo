from .models import Polygon
from rest_framework.generics import CreateAPIView

from .serializers import CreatePolygonSerializer


class PolygoneCreateAPIView(CreateAPIView):
    queryset = Polygon.objects.all()
    serializer_class = CreatePolygonSerializer

