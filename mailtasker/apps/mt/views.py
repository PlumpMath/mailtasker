from django.conf import settings

def create_mailing_list(user):
    return requests.post(
        "https://api.mailgun.net/v2/lists",
        auth=('api', settings.MAILGUN_KEY),
        data={'address': '%d@%s'%(user.id,settings.HOSTNAME)})

def add_member(owner, user):
    return requests.post(
        "https://api.mailgun.net/v2/lists/dev@samples.mailgun.org/members",
        auth=('api', settings.MAILGUN_KEY),
        data={'subscribed': True,
              'address': user.email,
              'name': user.name,
              #TODO 'vars': '{"age": 26}'},
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

# Handler for HTTP POST to http://myhost.com/messages for the route defined above
def on_incoming_message(request):
     if request.method == 'POST':
         sender    = request.POST.get('sender')
         recipient = request.POST.get('recipient')
         subject   = request.POST.get('subject', '')

         body_plain = request.POST.get('body-plain', '')
         body_without_quotes = request.POST.get('stripped-text', '')

         raise Exception("Look up! ^^")
         # note: other MIME headers are also posted here...

         # attachments:
         #for key in request.FILES:
         #    file = request.FILES[key]
             # do something with the file

     # Returned text is ignored but HTTP status code matters:
     # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
     return HttpResponse('OK')