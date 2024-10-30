from django.contrib import admin
from django.urls import path

from geo.views import PolygonDetailAPIView, PolygonCreateAPIView, PolygonCreateView, PolygonListAPIView, PolygonMapView

urlpatterns = [
    path('polygon/map/', PolygonMapView.as_view(), name='polygon_map'),
    path('polygons/', PolygonCreateView.as_view(), name='polygon_create'),
    path('polygons/list/', PolygonListAPIView.as_view(), name='polygons'),
    path('polygons/create/', PolygonCreateAPIView.as_view(), name='polygon_create_api'),
    path('polygons/<int:pk>/', PolygonDetailAPIView.as_view(), name='polygon'),
]
