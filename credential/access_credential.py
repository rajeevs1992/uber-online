from django.conf import settings

UBER_CLIENT_ID = '8GVIjNEt6iihwpqbPTM4MTrrCm0PKQ4H'
UBER_CLIENT_SECRET = 'ei9i8fe63Wahk2b2APrwhB_2M7s54k6X_Mp6yDcf'
UBER_SERVER_TOKEN = 'YZJ4F8u5L-ZyWQqp2MxsMZAaLcsgggl8jqd-Xi1N'

UBER_LOGIN_URL = 'https://login.uber.com/oauth/v2/authorize'
UBER_AUTH_URL = 'https://login.uber.com/oauth/v2/token'

API_URL = 'https://sandbox-api.uber.com'
REDIRECT_URI = 'http://localhost:8000/ride/action'

if not settings.DEBUG:
    API_URL = 'https://api.uber.com'
    REDIRECT_URI = 'https://uber-online.herokuapp.com/ride/action'