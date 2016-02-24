import urllib
import requests
from credential import access_credential as cred

def make_request(method, target, params, form, headers):
    api = cred.UBER_API_URL
    

