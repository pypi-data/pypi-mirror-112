import requests
import http.cookiejar
from pathlib import Path
import os, stat


class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return "ApiError: {}".format(vars(self.resp))

    
class Session():

    def __init__(self, cookie_path):
        self.s = requests.Session()
        Path(cookie_path).parent.mkdir(parents=True, exist_ok=True)
        self.s.cookies = http.cookiejar.LWPCookieJar(cookie_path)
        try:
            self.s.cookies.load(ignore_discard=True, ignore_expires=True)
        except FileNotFoundError:
            pass

    def _url(path):
        return 'https://api.simpel.nl/' + path

    def close(self):
        self.s.close()

    def save(self):
        self.s.cookies.save(ignore_discard=True, ignore_expires=True)
        os.chmod(self.s.cookies.filename, stat.S_IREAD | stat.S_IWRITE)

    def login(self, username, password):
        resp = self.s.post(Session._url('login'), json={
            "username": username,
            "password": password,
            "remember": True
        })
        if resp.status_code != 200:
            raise ApiError(resp)
        else:
            self.save()
            return True

    def account_subscription_overview(self):
        resp = self.s.get(Session._url('account/subscription-overview'))
        if resp.status_code != 200:
            raise ApiError(resp)
        else:
            self.save()
            return resp.json()

    def subscription(self, subscription_id):
        return Subscription(self, subscription_id)

class Subscription():

    def __init__(self, session, sid):
        self.s = session
        self.sid = sid

    def _url(path):
        return 'https://mijn.simpel.nl/api/' + path

    def get(self, path):
        resp = self.s.s.get(Subscription._url(path), params={
            "sid": self.sid
        })
        if resp.status_code != 200:
            raise ApiError(resp)
        else:
            self.s.save()
            return resp.json()            
        
    def dashboard(self):
        return self.get('dashboard')

    def products(self):
        return self.get('subscription/products')

    def ceiling(self):
        return self.get('subscription/ceiling')

    def usage_summary(self):
        return self.get('usage/usage-summary')

    def usage_other_costs(self):
        return self.get('usage/other-costs')

    def usage_cdrs(self):
        return self.get('usage/cdrs')

    def latest_invoice(self):
        return self.get('invoice/latest')

    def correction_for_billing_period(self):
        return self.get('correction/for-billing-period')
