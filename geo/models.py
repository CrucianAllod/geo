from django.contrib.gis.db import models

class Polygon(models.Model):
    """Модель для хранения информации о полигоне."""

    name: str = models.CharField(max_length=255)
    polygon: models.PolygonField = models.PolygonField()
    crosses_antimeridian: bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Возвращает строковое представление полигона.

        Returns:
            str: Имя полигона.
        """
        return self.name