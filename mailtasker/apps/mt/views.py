import logging

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Handler for HTTP POST to http://HOSTNAME/messages for the route defined above
@csrf_exempt
def incoming_message(request):
     if request.method == 'POST':
        sender_email         = request.POST.get('sender')
        sender, created      = User.objects.get_or_create(email=sender_email)
        list_name            = request.POST.get('subject', '')
        task_list, created   = TaskList.objects.get_or_create(
                                            email=sender_email,
                                            name=list_name,
                                            )
        body                  = request.POST.get('stripped-text', '')

     return HttpResponse('OK')