from lib2to3.fixes.fix_input import context

from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.views.generic import FormView, TemplateView
from django.urls import reverse
import folium
from django.db.models import F
from folium import Polygon
from numpy.polynomial.polynomial import polyone

from .forms import PolygonForm
from .models import Polygon as mPolygon
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from .serializers import PolygonCreateSerializer, PolygonDetailSerializer, PolygonListSerializer


class PolygonMapView(TemplateView):
    """View для отображения карты с полигонами."""

    template_name: str = 'polygon_map.html'

    def get_context_data(self, **kwargs) -> dict:
        """Добавляет полигоны на карту и возвращает контекст для шаблона.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            dict: Контекст для шаблона с картой.
        """
        context = super().get_context_data(**kwargs)
        polygons = mPolygon.objects.all()
        map = folium.Map(location=[0, 0], zoom_start=2)

        for polygon in polygons:
            coords = list(polygon.polygon.coords[0])
            folium.Polygon(locations=[(lat, lon) for lon, lat in coords], color='blue', fill=True, ill_opacity=0.5).add_to(map)

        context['map'] = map._repr_html_()

        return context


class PolygonCreateView(FormView):
    """View для создания полигона с формой."""

    template_name: str = 'polygon_form.html'
    form_class = PolygonForm

    def form_valid(self, form) -> JsonResponse:
        """Обрабатывает валидную форму, создает полигон и возвращает ответ.

        Args:
            form (PolygonForm): Валидная форма с данными о полигоне.

        Returns:
            JsonResponse: Ответ с данными о созданном полигоне или редирект.
        """
        print(form.cleaned_data)
        name: str = form.cleaned_data['name'].strip()
        coordinates: list[str] = form.cleaned_data['coordinates'].strip().splitlines()

        # Проверка на пустое имя
        if not name:
            return JsonResponse({'error': 'Polygon name cannot be empty.'}, status=400)

        coords: list[tuple[float, float]] = []
        for coord in coordinates:
            try:
                lat, lon = map(float, coord.split(','))
                coords.append((lon, lat))
            except ValueError:
                return JsonResponse({'error': 'Invalid coordinate format. Use "latitude,longitude".'}, status=400)

        longitudes: list[float] = [lon for lon, lat in coords]
        crosses_antimeridian: bool = (max(longitudes) > 0 and min(longitudes) < 0)

        if crosses_antimeridian:
            coords = [(lon - 360 if lon > 180 else lon + 360 if lon < -180 else lon, lat) for lat, lon in coords]

        polygon_geom = GEOSGeometry(f'POLYGON(({", ".join(f"{lon} {lat}" for lon, lat in coords)}))')
        mPolygon.objects.create(name=name, polygon=polygon_geom, crosses_antimeridian=crosses_antimeridian)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return self.get_polygons_as_json()
        return redirect(reverse('polygon_create'))

    def get_context_data(self, **kwargs) -> dict:
        """Добавляет сохраненные полигоны в контекст.

        Args:
            **kwargs: Дополнительные аргументы.

        Returns:
            dict: Контекст для шаблона с сохраненными полигонами.
        """
        context = super().get_context_data(**kwargs)
        context['polygons'] = mPolygon.objects.all()
        return context

    def get_polygons_as_json(self) -> JsonResponse:
        """Возвращает список полигонов в формате JSON.

        Returns:
            JsonResponse: Список полигонов в формате JSON.
        """
        polygons = list(
            mPolygon.objects.annotate(
                polygon_wkt=F('polygon')
            ).values('name', 'polygon_wkt', 'crosses_antimeridian')
        )

        for polygon in polygons:
            polygon['polygon'] = polygon['polygon_wkt'].wkt if polygon['polygon_wkt'] else None
            polygon.pop('polygon_wkt')

        return JsonResponse(polygons, safe=False)

class PolygonCreateAPIView(CreateAPIView):
    """API View для создания полигона."""

    queryset = mPolygon.objects.all()
    serializer_class = PolygonCreateSerializer


class PolygonDetailAPIView(RetrieveUpdateDestroyAPIView):
    """API View для получения, обновления и удаления полигона."""

    queryset = mPolygon.objects.all()
    serializer_class = PolygonDetailSerializer


class PolygonListAPIView(ListAPIView):
    """API View для получения списка полигонов."""

    queryset = mPolygon.objects.all()
    serializer_class = PolygonListSerializer