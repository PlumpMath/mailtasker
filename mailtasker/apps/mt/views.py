import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Handler for HTTP POST to http://myhost.com/messages for the route defined above
@csrf_exempt
def incoming_message(request):
     if request.method == 'POST':
         sender    = request.POST.get('sender')
         recipient = request.POST.get('recipient')
         subject   = request.POST.get('subject', '')

         body_plain = request.POST.get('body-plain', '')
         body_without_quotes = request.POST.get('stripped-text', '')

         logging.exception("Look up! ^^")
         # note: other MIME headers are also posted here...

         # attachments:
         #for key in request.FILES:
         #    file = request.FILES[key]
             # do something with the file

     # Returned text is ignored but HTTP status code matters:
     # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
     return HttpResponse('OK')