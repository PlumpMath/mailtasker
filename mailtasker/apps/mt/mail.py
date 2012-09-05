#FRAMEWORK
from django.conf import settings

#LIB
import requests
from orderedmultidict import omdict as MultiDict


def create_mailing_list(user):
    return requests.post(
        "https://api.mailgun.net/v2/lists",
        auth=('api', settings.MAILGUN_KEY),
        data={'address': '%d@%s'%(user.id,settings.HOSTNAME)}
        )

def add_member(owner, user):
    return requests.post(
        "https://api.mailgun.net/v2/lists/dev@samples.mailgun.org/members",
        auth=('api', settings.MAILGUN_KEY),
        data={'subscribed': True,
              'address': user.email,
              'name': user.name,
              #TODO 'vars': '{"age": 26}'},
              }
        )

def post_message(tasklist, body):
    r = requests.\
        post(("https://api.mailgun.net/v2/samples.mailgun.org/"
              "messages"),
             auth=("api", settings.MAILGUN_KEY),
             data={
                 "from": "MailTasker <app@mailtasker.com>",
                 "to": [tasklist.id],
                 "subject": tasklist.name,
                 "text": body
                 }
             )
    return r

def create_route():
    r = requests.\
        post("https://api.mailgun.net/v2/routes",
             auth=("api", settings.MAILGUN_KEY),
             data=MultiDict([
                 ("priority", 1),
                 ("description", "Incoming route"),
                 ("expression",
                "match_recipient('.*@%s')"%settings.HOSTNAME),
                 ("action",
                    "forward('http://%s/messages/')"%settings.HOSTNAME),
                 ("action", "stop()"),
                 ])
             )
    return r