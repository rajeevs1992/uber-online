from django import forms
from ride.models import Destination

class RequestForm(forms.Form):
    from_latitude = forms.CharField(max_length=50)
    from_longitude = forms.CharField(max_length=50)

    to_latitude = forms.CharField(max_length=50, required=False)
    to_longitude = forms.CharField(max_length=50, required=False)

    destination = forms.ModelChoiceField(queryset=Destination.objects.none(),
                                         label='Or choose detination from dropdown',
                                         required=False)

    def __init__(self, user, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['destination'].queryset = Destination.objects.filter(user=user)

