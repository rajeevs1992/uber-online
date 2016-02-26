from django import forms
from ride.models import Destination

class RequestForm(forms.Form):
    source = forms.ModelChoiceField(queryset=Destination.objects.none(),
                                         label='Choose source from dropdown or enter manually',
                                         required=False)

    from_latitude = forms.DecimalField(max_digits=30, decimal_places=6, required=False)
    from_longitude = forms.DecimalField(max_digits=30, decimal_places=6, required=False)

    destination = forms.ModelChoiceField(queryset=Destination.objects.none(),
                                         label='Choose detination from dropdown or enter manually',
                                         required=False)

    to_latitude = forms.DecimalField(max_digits=30, decimal_places=6, required=False)
    to_longitude = forms.DecimalField(max_digits=30, decimal_places=6, required=False)

    def __init__(self, user, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.filter(user=user)
        self.fields['source'].queryset = Destination.objects.filter(user=user)
