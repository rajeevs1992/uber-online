import urllib
import requests
import datetime

from ride.forms import RequestForm
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ride.models import Request, BookingDetails
from cab.models import Cab
from credential.models import UberCredential
from credential import access_credential as cred

@login_required
def index(request):
    if request.method == 'GET':
        pending = Request.objects.filter(user=request.user, pending=True)
        if pending:
            if pending.first().requestid:
                return redirect('status')
            pending.update(pending=False)
        return render(request, 'request.html', {'form' : RequestForm(request.user)})
    else:
        form = RequestForm(request.user, request.POST)
        if not form.is_valid():
            return render(request, 'request.html', {'form' : form})
        
        to_latitude = to_longitude = None
        if form.cleaned_data['destination']:
            to_latitude = form.cleaned_data['destination'].latitude
            to_longitude = form.cleaned_data['destination'].longitude
        elif form.cleaned_data['to_latitude'] and form.cleaned_data['to_longitude']:
            to_latitude = form.cleaned_data['to_latitude']
            to_longitude = form.cleaned_data['to_longitude']
        else:
            form.add_error('destination', 'Specify destination coords or choose from dropdown')
            return render(request, 'request.html', {'form' : form})

        from_latitude = from_longitude = None
        if form.cleaned_data['source']:
            from_latitude = form.cleaned_data['source'].latitude
            from_longitude = form.cleaned_data['source'].longitude
        elif form.cleaned_data['from_latitude'] and form.cleaned_data['from_longitude']:
            from_latitude = form.cleaned_data['from_latitude']
            from_longitude = form.cleaned_data['from_longitude']
        else:
            form.add_error('source', 'Specify source coords or choose from dropdown')
            return render(request, 'request.html', {'form' : form})

        req = Request()
        req.user = request.user
        req.from_latitude = from_latitude
        req.from_longitude = from_longitude
        req.to_latitude = to_latitude
        req.to_longitude = to_longitude
        req.pending = True
        req.book_date = datetime.datetime.now()
        req.save()
        return redirect('select')

@login_required
def select(request):
    if request.method == 'GET':
        req = Request.objects.filter(user=request.user, pending=True).first()
        if req is None:
            return redirect('request')
        credential = UberCredential.objects.filter(user=request.user).first()
        if credential is None:
            params = {}
            params['response_type'] = 'code'
            params['client_id'] = cred.UBER_CLIENT_ID
            params['scope'] = 'profile request'
            params['redirect_uri'] = settings.REDIRECT_URI + '/auth'
            return redirect(cred.UBER_LOGIN_URL + '?' + urllib.urlencode(params))
        args = {}
        args['req'] = req
        args['products'] = get_products(req, request)
        return render(request, 'select.html', args)

def get_products(req, request):
    api = settings.API_URL + '/v1/products'
    params = {}
    params['server_token'] = cred.UBER_SERVER_TOKEN
    params['latitude'] = req.from_latitude
    params['longitude'] = req.from_longitude
    response = requests.get(api, params=params)
    if response.status_code == 200:
        products = response.json()
        credential = UberCredential.objects.get(user=request.user)
        headers = {}
        headers['Authorization'] = 'Bearer ' + credential.access_token
        params = {}
        params['start_latitude'] = req.from_latitude
        params['start_longitude'] = req.from_longitude
        response = requests.get(settings.API_URL + '/v1/estimates/time', params=params, headers=headers)
        times = {}
        if response.status_code == 200:
            times = response.json()
            if 'times' in times:
                for product in times['times']:
                    times[product['product_id']] = product['estimate']
        res = []
        for p in products['products']:
            c = Cab(p)
            if c.product_id in times:
                c.eta = times[c.product_id]/60
            res.append(c)
        return res
    else:
        return []

@login_required
def action(request, target):
    if target == 'auth':
        authorization_code = request.GET['code']
        params = {}
        params['client_secret'] = cred.UBER_CLIENT_SECRET
        params['client_id'] = cred.UBER_CLIENT_ID
        params['grant_type'] = 'authorization_code'
        params['redirect_uri'] = settings.REDIRECT_URI + '/auth'
        params['code'] = authorization_code

        response = requests.post(cred.UBER_AUTH_URL,
                                 data=params)
        if response.status_code != 200:
            response = response.json()
            messages.error(request, response)
            return redirect('request')
        # Ensure single user
        UberCredential.objects.filter(user=request.user).delete()
        response = response.json()
        credential = UberCredential()
        credential.user = request.user
        credential.authorization_code = authorization_code.strip()
        credential.access_token = response.get('access_token').strip()
        credential.refresh_token = response.get('refresh_token').strip()
        credential.expires_in = response.get('expires_in')
        credential.scope = response.get('scope').strip()
        credential.created_date = datetime.datetime.now()
        credential.save()
        return redirect('select')
    elif target == 'surge':
        req = Request.objects.filter(user=request.user, pending=True)
        if req:
            return redirect('book', productid=req.first().productid)
    elif target == 'reauth':
        UberCredential.objects.filter(user=request.user).delete()
        params = {}
        params['response_type'] = 'code'
        params['client_id'] = cred.UBER_CLIENT_ID
        params['scope'] = 'profile request'
        params['redirect_uri'] = settings.REDIRECT_URI + '/auth'
        return redirect(cred.UBER_LOGIN_URL + '?' + urllib.urlencode(params))
    return redirect('request')

@login_required
def book(request, productid):
    api = settings.API_URL + '/v1/requests'
    credential = UberCredential.objects.get(user=request.user)
    req = Request.objects.filter(user=request.user, pending=True)
    if not req:
        return redirect('request')
    req = req.first()
    if req.requestid is None:
        req.productid = productid
        headers = {}
        headers['Authorization'] = 'Bearer ' + credential.access_token
        headers['Content-Type'] = 'application/json'
        params = {}
        params['start_latitude'] = req.from_latitude
        params['start_longitude'] = req.from_longitude
        params['end_latitude'] = req.to_latitude
        params['end_longitude'] = req.to_longitude
        params['product_id'] = productid
        if req.surge_confirmation_id:
            params['surge_confirmation_id'] = req.surge_confirmation_id

        response = requests.post(api, json=params, headers=headers)
        if response.status_code == 202:
            req.requestid = response.json().get('request_id')
            req.save()
            return redirect('status')
        elif response.status_code == 409:
            r = response.json()
            if 'surge_confirmation' in r['meta']:
                req.surge_confirmation_id = r['meta']['surge_confirmation']['surge_confirmation_id']
                req.save()
                return redirect(r['meta']['surge_confirmation']['href'])
        else:
            messages.error(request, response.json())
            return redirect('request')
    else:
        return redirect('status')

@login_required
def delete(request):
    r = Request.objects.filter(user=request.user, pending=True)
    if not r:
        messages.info(request, 'No active rides to delete')
        return redirect('request')
    r = r.first()
    credential = UberCredential.objects.get(user=request.user)
    headers = {}
    headers['Authorization'] = 'Bearer ' + credential.access_token
    api = settings.API_URL + '/v1/requests/' + r.requestid
    response = requests.delete(api, headers=headers)
    if response.status_code == 204:
        r.pending = False
        r.save()
        messages.success(request, 'Ride cancelled')
        return redirect('request')
    else:
        messages.error(request, response.json())
        return redirect('status')

@login_required
def status(request):
    api = settings.API_URL + '/v1/requests/'
    r = Request.objects.filter(user=request.user, pending=True)
    if not r:
        return redirect('request')
    r = r.first()
    credential = UberCredential.objects.get(user=request.user)
    headers = {}
    headers['Authorization'] = 'Bearer ' + credential.access_token
    response = requests.get(api + r.requestid, headers=headers)

    if response.status_code == 200:
        args = {}
        response = response.json()
        if response['status'] == 'completed':
            r.pending = False
            r.save()
            messages.info(request, 'Ride completed')
            return redirect('request')
        args['req'] = r
        args['details'] = BookingDetails(response)
        return render(request, 'status.html', args)
    else:
        r.pending = False
        r.save()
        messages.error(request, response.json())
        return redirect('request')
