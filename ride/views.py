import urllib

from ride.forms import RequestForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

def index(request):
    if request.method == 'GET':
        return render(request, 'request.html', {'form' : RequestForm()})
    else:
        form = RequestForm(request.POST)
        if not form.is_valid():
            return render(request, 'request.html', {'form' : form},)
        args = {}
        args['latitude'] = form.cleaned_data['latitude']
        args['longitude'] = form.cleaned_data['longitude']
        args['cabtype'] = form.cleaned_data['cab_type'].id
        return redirect(reverse('confirm') + '?' + urllib.urlencode(args))

def confirm(request):
    if request.method == 'GET':
        return render(request, 'confirm.html', {})
    else:
        return None
