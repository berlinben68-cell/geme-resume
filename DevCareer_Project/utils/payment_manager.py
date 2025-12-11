import requests

class PaymentManager:
    def __init__(self, razorpay_key=None, stripe_key=None):
        self.razorpay_key = razorpay_key
        self.stripe_key = stripe_key

    def get_user_country(self, ip_address):
        """
        Mock function to get user country from IP.
        In production, use a GeoIP library or API.
        """
        # Mock logic
        if ip_address.startswith("10."): # Local/Private
            return "INDIA" 
        return "GLOBAL"

    def route_payment(self, user_ip, amount):
        country = self.get_user_country(user_ip)
        
        if country == "INDIA":
            return self._initiate_razorpay(amount)
        else:
            return self._initiate_stripe(amount)

    def _initiate_razorpay(self, amount):
        print(f"Initiating Razorpay for INR {amount}")
        return {
            "gateway": "razorpay",
            "currency": "INR",
            "amount": amount * 100, # Razorpay expects paisa
            "key": self.razorpay_key
        }

    def _initiate_stripe(self, amount):
        print(f"Initiating Stripe for USD {amount}")
        return {
            "gateway": "stripe",
            "currency": "USD",
            "amount": amount * 100, # Stripe expects cents
            "key": self.stripe_key
        }
