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
    message_id = models.CharField(max_length=250, blank=True, null=True, unique=True)

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
                #If this is an empty line then look no further
                break
            else:
                #Create a new task
                Task.objects.create(
                    task_list = self,
                    value = line.strip(),
                    order = self.task_set.filter(is_completed=False).count(),
                    )

    def notify(self):
        tasks = self.task_set.filter(is_completed=False)
        headers =  ['#','Task','Created']
        data = [[str(t.order), str(t.value), str(t.created.strftime('%Y%m%d'))] for t in tasks]
        data.insert(0,headers)
        col_width = max(len(word) for row in data for word in row) + 2  # padding
        body = ""
        for row in data:
            body += "".join(word.ljust(col_width) for word in row) + '\n'
        html = '<html><div>%s</div></html>'%body.replace('  ',
            """<span class=3D=22Apple-tab-span=22 style=3D=22=white-space:pre=22>     </span>""")\
                .replace('\n','</div><div>')
        post_message(self,body,html)

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
