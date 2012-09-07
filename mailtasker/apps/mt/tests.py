"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from apps.mt.models import TaskList, Task
from django.contrib.auth.models import User

from django.test import TestCase


class TaskListTests(TestCase):
    def test_process(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        user = User.objects.create(
            username="test",
            password="123",
            email="test@suite.com"
            )
        t = TaskList.objects.create(
            name="test",
            owner=user
            )

        self.assertEquals(Task.objects.count(),0)

        #TEST CREATION
        body = """hello
        i am
        three tasks

        not me!
        """
        t.process(body)
        self.assertEquals(Task.objects.count(),3)

        #TEST COMPLETION
        body = """hello
        1,2,0

        not me!
        """
        t.process(body)

        self.assertEquals(Task.objects.filter(completed__isnull=True).count(),1)