from __future__ import unicode_literals

from django.db import models

class Cab:
    
    def __init__(self, product):
        self.capacity = product['capacity']
        self.description = product['description']
        self.distance_unit = product['price_details']['distance_unit']
        self.cpm = product['price_details']['cost_per_minute']
        self.minimum = product['price_details']['minimum']
        self.cpd = product['price_details']['cost_per_distance']
        self.base = product['price_details']['base']
        self.cancellation_fee = product['price_details']['cancellation_fee']
        self.currency_code = product['price_details']['currency_code']
        self.image = product['image']
        self.display_name = product['display_name']
        self.product_id = product['product_id']
        self.eta = None
