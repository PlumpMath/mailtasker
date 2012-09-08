from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string

import pretty

from apps.mt.mail import post_message, post_list_message

class TaskManager(models.Manager):
    def render_all(self, owner):
        lists = super(TaskManager, self).get_query_set().filter(owner=owner)
        body = render_to_string('all_lists_plain_text.html', {'lists':lists})
        html = render_to_string('all_lists.html', {'lists':lists})
        return body, html

    def notify_all(self, owner):
        body, html = self.render_all(owner=owner)
        post_message(owner.email,'MailTasker Daily Update',body,html)


class TaskList(models.Model):
    """
        A list of tasks parse from email
    """
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True)
    message_id = models.CharField(max_length=250, blank=True, null=True, unique=True)
    objects = TaskManager()

    unique_together = ("name", "owner")

    def process(self, body):
        """
        """
        #Parse the tasks
        #Create them
        #If a line is just a numbers or commas then complete them
        for line in body.split('\n'):
            if line.replace(',','').replace(' ','').isdigit():
                #This line contains only digits and possibly commas or spaces
                #Parse them into a list
                if ',' in line:
                    for i in line.split(','):
                        tasks = [int(i.strip()) for i in line.split(',')]
                elif ' ' in line:
                    for i in line.split(' '):
                        tasks = [int(i.strip()) for i in line.split(' ')]
                else:
                    tasks = [int(line)]
                #Complete the relevant Tasks
                self.task_set.filter(order__in=tasks).update(completed=datetime.now())
            elif line.isspace() or len(line)==0:
                #If this is an empty line then look no further
                break
        for line in body.split('\n'):
            if line.isspace() or len(line)==0:
                #If this is an empty line then look no further
                break
            if not line.replace(',','').replace(' ','').isdigit():
                #Create a new task
                Task.objects.create(
                    task_list = self,
                    value = line.strip(),
                    order = self.task_set.count(),
                    )

    def render(self):
        tasks = self.task_set.filter(completed__isnull=True)
        body = render_to_string('email_plain_text.html', {'tasks':tasks})
        html = render_to_string('email.html', {'tasks':tasks})
        return body, html

    def notify(self, body=None, html=None, message_id=None):
        if not body or not html:
            body, html = self.render()
        post_list_message(self,body,html,message_id=message_id)

class Task(models.Model):
    """
        A single task
    """
    task_list = models.ForeignKey(TaskList)
    value = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    completed = models.DateTimeField(blank=True,null=True)

    def created_pretty(self):
        return pretty(getattr(self,'created'))

    def completed_pretty(self):
        return pretty(getattr(self,'completed'))
