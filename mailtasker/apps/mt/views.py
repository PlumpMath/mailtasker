import logging

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from apps.mt.models import TaskList
from apps.mt.mail import create_mailing_list, add_member

# Handler for HTTP POST to http://HOSTNAME/messages for the route defined above
@csrf_exempt
def incoming_message(request):
     if request.method == 'POST':
        sender_email         = request.POST.get('sender')
        logging.info(sender_email)
        owner, created      = User.objects.get_or_create(email=sender_email)
        list_name            = request.POST.get('subject', '')

        logging.info(list_name)
        tasklist, created   = TaskList.objects.get_or_create(
                                            owner=owner,
                                            name=list_name,
                                            )
        if created:
            create_mailing_list(tasklist)
            add_member(tasklist, owner)
        body                  = request.POST.get('stripped-text', '')
        tasklist.process(body)
        tasklist.notify()

     return HttpResponse('OK')