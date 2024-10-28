from django import forms
from .models import Polygon


class PolygoneForm(forms.ModelForm):
    model = Polygon
    class Meta:
        fields = '[name, polygon]'