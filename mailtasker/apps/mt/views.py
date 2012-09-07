from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from apps.mt.models import TaskList
from apps.mt.mail import create_mailing_list, add_member

# Handler for HTTP POST to http://HOSTNAME/messages for the route defined above
@csrf_exempt
def incoming_message(request):
    """
    Handle an incoming email, creating the relevant objects
    and retrieving the specified TaskList
    """
    if request.method == 'POST':
        sender_email         = request.POST.get('sender')
        name                 = request.POST.get('from').split('<')[0].strip()
        owner, created       = User.objects.get_or_create(
                                    username=sender_email,
                                    email=sender_email,
                                    first_name=name,
                                    )
        message_id = request.POST.get('Message-Id')

        list_name            = request.POST.get('subject', '')
        if ':' in list_name:
            #Strip out anything before the last colon inclusive
            #This removes Re:Re: and Fwd: etc.
            list_name = list_name[list_name.rindex(':')+1:]
        list_name = list_name.strip()

        if list_name == 'all' or '':
            #Send all uncompleted tasks from all TaskLists
            TaskList.objects.notify_all(owner=owner)
            return HttpResponse('OK')

        tasklist, created   = TaskList.objects.get_or_create(
                                            owner=owner,
                                            name=list_name,
                                            )
        if created:
            create_mailing_list(tasklist)
            add_member(tasklist, owner)
            tasklist.message_id = message_id
        body                    = request.POST.get('stripped-text', '')
        tasklist.process(body)
        tasklist.notify(message_id=message_id)

    return HttpResponse('OK')
