import requests

from django.conf import settings

def send_message(email_from, email_subject, email_body,  email_to=[]):
    return requests.post(
        "%s/messages" % settings.MAILGUN_API_BASE_URL,
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": email_from,
              "to": email_to,
              "subject": email_subject,
              "text": email_body})