#FRAMEWORK
from django.conf import settings

#LIB
import requests
from orderedmultidict import omdict as MultiDict


def create_mailing_list(tasklist):
    return requests.post(
        "https://api.mailgun.net/v2/lists",
        auth=('api', settings.MAILGUN_KEY),
        data={'address': 'tl#%d@%s'%(tasklist.id,settings.HOSTNAME)}
        )

def add_member(tasklist, user):
    return requests.post(
        "https://api.mailgun.net/v2/lists/tl#%d@%s/members"%(tasklist.id,settings.HOSTNAME),
        auth=('api', settings.MAILGUN_KEY),
        data={'subscribed': True,
              'address': user.email,
              'name': user.first_name,
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
                 "to": ['tl#%d@%s'%(tasklist.id,settings.HOSTNAME)],
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
                "match_recipient('app@%s')"%settings.HOSTNAME),
                 ("action",
                    "forward('http://%s/messages/')"%settings.HOSTNAME),
                 ("action", "stop()"),
                 #"match_recipient('tl#(?P<tasklist_id>\d+)@%s')"%settings.HOSTNAME),
                 ])
             )
    return r