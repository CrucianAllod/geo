from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers

from geo.models import Polygon


class PolygonFieldSerializer(serializers.Field):
    """Сериализатор для поля полигона."""

    child = serializers.ListField(child=serializers.FloatField())

    def to_representation(self, value: GEOSGeometry) -> list[list[float]]:
        """Преобразует объект полигона в представление.

        Args:
            value (GEOSGeometry): Объект полигона.

        Returns:
            list[list[float]]: Список координат полигона.
        """
        return [[float(x), float(y)] for x, y in value.coords[0]]

    def to_internal_value(self, data: str) -> GEOSGeometry:
        """Преобразует входные данные в объект полигона.

        Args:
            data (str): Строка, представляющая полигон.

        Returns:
            GEOSGeometry: Объект полигона.

        Raises:
            serializers.ValidationError: Если данные не являются строкой или имеют неверный формат.
        """
        if not isinstance(data, str):
            raise serializers.ValidationError("Value must be a string representing a polygon.")
        try:
            return GEOSGeometry(data)
        except Exception as e:
            raise serializers.ValidationError(f"Invalid polygon format: {str(e)}")


class PolygonCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания полигона."""

    polygon = PolygonFieldSerializer()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Polygon
        fields = ['id', 'name', 'polygon', 'crosses_antimeridian']


class PolygonDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для деталей полигона."""

    polygon = PolygonFieldSerializer()

    class Meta:
        model = Polygon
        fields = ['id', 'name', 'polygon', 'crosses_antimeridian']


class PolygonListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка полигонов."""

    polygon = PolygonFieldSerializer()

    class Meta:
        model = Polygon
        fields = ['id', 'name', 'polygon', 'crosses_antimeridian']