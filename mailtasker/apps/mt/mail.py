#FRAMEWORK
from django.conf import settings

#LIB
import requests
from orderedmultidict import omdict as MultiDict


def create_mailing_list(tasklist):
    return requests.post(
        "https://api.mailgun.net/v2/lists",
        auth=('api', settings.MAILGUN_KEY),
        data={'address': 'task_list%d@%s'%(tasklist.id,settings.HOSTNAME)}
        )

def add_member(tasklist, user):
    return requests.post(
        "https://api.mailgun.net/v2/lists/task_list%d@%s/members"%(tasklist.id,settings.HOSTNAME),
        auth=('api', settings.MAILGUN_KEY),
        data={'subscribed': True,
              'address': user.email,
              'name': user.first_name,
              #TODO 'vars': '{"age": 26}'},
              }
        )

def post_message(tasklist, body, html=None):

    r = requests.\
        post(("https://api.mailgun.net/v2/%s/messages"%settings.HOSTNAME),
             auth=("api", settings.MAILGUN_KEY),
             data={
                 "from": "MailTasker <app@mailtasker.com>",
                 "to": ['task_list%d@%s'%(tasklist.id,settings.HOSTNAME)],
                 "subject": 'Re: %s'%tasklist.name,
                 "text": body,
                 "html": html,
                 "h:In-Reply-To": tasklist.message_id or '',
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
                 #"match_recipient('task_list(?P<tasklist_id>\d+)@%s')"%settings.HOSTNAME),
                 ])
             )
    return r