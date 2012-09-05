from django.conf import settings

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

def create_route():
    r = requests.\
        post("https://api.mailgun.net/v2/routes",
             auth=("api", settings.MAILGUN_KEY),
             data=MultiDict([
                 ("priority", 1),
                 ("description", "Incoming route"),
                 ("expression",
                  "match_recipient('.*@%s)"%settings.HOSTNAME),
                 ("action",
                  "forward('http://%s/messages/')"%settings.HOSTNAME),
                 ("action", "stop()")
                 ]))
    return r