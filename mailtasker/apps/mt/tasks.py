from django.contrib.auth.models import User

@task
def notify_all_users():
    """
    """
    for user in User.objects.all():
        user.tasklist_set.all().notify_all()

