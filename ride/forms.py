from django import forms
from cab.models import CabType

class RequestForm(forms.Form):
    latitude = forms.CharField(max_length=50)
    longitude = forms.CharField(max_length=50)
    cab_type = forms.ModelChoiceField(queryset=CabType.objects.all().order_by('name'))
