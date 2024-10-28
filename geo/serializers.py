from rest_framework import serializers

from geo.models import Polygon


class CreatePolygonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = '[name, polygon, crosses_antimeridian]'
