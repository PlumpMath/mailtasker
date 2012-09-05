from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from apps.mt.mail import post_message

def _fmtcols(mylist, cols):
    #http://stackoverflow.com/questions/171662/formatting-a-list-of-text-into-columns
    lines = ("\t".join(mylist[i:i+cols]) for i in xrange(0,len(mylist),cols))
    return '\n'.join(lines)


class TaskList(models.Model):
    """
        A list of tasks parse from email
    """
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User)
    created = models.DateTimeField(auto_now=True)

    def process(self, body):
        """
        """
        #Parse the tasks
        #Create them
        #If a line is just a numbers or commas then complete them
        for line in body.split('\n'):
            if line.replace(',','').replace(' ','').isdigit():
                #This line contains only digits and possibly commas or spaces
                if ',' in line:
                    tasks = [int(i.strip()) for i in line.split(',')]
                elif ' ' in line:
                    tasks = [int(i.strip()) for i in line.split(' ')]
                else:
                    tasks = [int(line.strip())]
                for task in tasks:
                    task.completed = datetime.now()
                    task.is_completed = True
            elif line.isspace() or len(line)==0:
                continue
            else:
                #Create a new task
                Task.objects.create(
                    task_list = self,
                    value = line.strip(),
                    order = self.task_set.filter(is_completed=False).count(),
                    )

    def notify(self):
        tasks = self.task_set.filter(is_completed=False)
        tl =  ['#','Task','Created']
        for t in tasks:
            tl.append(str(t.order))
            tl.append(str(t.value))
            tl.append(str(t.created.strftime('%Y%m%d')))
        body = _fmtcols(tl,3)
        post_message(self,body)

class Task(models.Model):
    """
        A single task
    """
    task_list = models.ForeignKey(TaskList)
    value = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    completed = models.DateTimeField(blank=True,null=True)
    is_completed = models.BooleanField()
