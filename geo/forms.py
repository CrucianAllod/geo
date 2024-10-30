from django import forms

class PolygonForm(forms.Form):
    """Форма для создания полигона."""

    name: str = forms.CharField(max_length=255)
    coordinates: str = forms.CharField(widget=forms.Textarea)