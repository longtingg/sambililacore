import requests
import json
from django.conf import settings

USE_MAILCHIMP = getattr(settings, 'USE_MAILCHIMP', False)

if USE_MAILCHIMP:
    MAILCHIMP_API_KEY = getattr(settings, 'MAILCHIMP_API_KEY', '')
    MAILCHIMP_DATA_CENTER = getattr(settings, 'MAILCHIMP_DATA_CENTER', '')
    MAILCHIMP_LIST_ID = getattr(settings, 'MAILCHIMP_LIST_ID', '')
    API_URL = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
    memebers_endpoint = f'{API_URL}/lists/{MAILCHIMP_LIST_ID}/members'
else:
    MAILCHIMP_API_KEY = ''
    memebers_endpoint = ''


def subscribe(email):
    if not USE_MAILCHIMP:
        return None, None
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    try:
        r = requests.post(
            memebers_endpoint,
            auth=("", MAILCHIMP_API_KEY),
            data=json.dumps(data)
        )
        return r.status_code, r.json()
    except Exception:
        raise Exception("Mailchimp is not configured properly.")
