from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from core.models import Task
from core.views import TaskViewSet


class TestTask(TestCase):
    def test_task_is_done(self):
        task = Task(status='done')
        self.assertTrue(task.is_done)

    def test_task_is_not_done(self):
        task = Task(status='open')
        self.assertFalse(task.is_done)


class TestTaskAPI(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='john_doe')
        self.view = TaskViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})

    def do_request(self, request, **kwargs):
        force_authenticate(request, user=self.user)
        response = self.view(request, **kwargs)
        return response

    def test_all_users_can_see_list_of_all_tasks(self):
        own_task = Task.objects.create(created_by=self.user, name="my own task")
        janes_task = Task.objects.create(created_by=User.objects.create(username='jane'), name="jane's task")
        request = self.factory.get('/tasks/')
        response = self.do_request(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {'name': "my own task", 'description': '', 'id': own_task.pk, 'status': 'open', 'is_own': True,
             'created_by': 'john_doe', 'completed_by': None},
            {'name': "jane's task", 'description': '', 'id': janes_task.pk, 'status': 'open', 'is_own': False,
             'created_by': 'jane', 'completed_by': None}
        ])

    def test_task_is_created_and_creator_is_set(self):
        request = self.factory.post('/tasks/', {'name': 'new task'}, format='json')
        response = self.do_request(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data,
                         {'name': 'new task', 'description': '', 'id': 1, 'status': 'open', 'is_own': True,
                          'created_by': 'john_doe', 'completed_by': None})

    def test_task_creation_requires_name(self):
        request = self.factory.post('/tasks/', {}, format='json')
        response = self.do_request(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'name': ['This field is required.']})

    def test_task_completed_by_user(self):
        task = Task.objects.create(created_by=User.objects.create(username='jane'), name="new task")
        request = self.factory.post('/tasks/%d/done/' % task.pk, format='json')
        force_authenticate(request, user=self.user)
        response = TaskViewSet.as_view({'post': 'complete'})(request, pk=task.pk)

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(task.is_done)
        self.assertEqual(
            response.data,
            {'name': 'new task', 'description': '', 'id': task.pk, 'status': 'done', 'is_own': False,
             'created_by': 'jane', 'completed_by': 'john_doe'},
        )

    def test_task_can_be_edited_by_only_creator(self):
        task = Task.objects.create(created_by=User.objects.create(username='jane'), name="jane's task")
        request = self.factory.put('/tasks/%d/' % task.pk, {'name': 'new name'}, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=task.pk)

        self.assertEqual(response.status_code, 404)

    def test_task_is_deleted_by_creator(self):
        task = Task.objects.create(created_by=self.user, name="new task")
        request = self.factory.delete('/tasks/%d/' % task.pk)
        response = self.do_request(request, pk=task.pk)

        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
        self.assertEqual(response.status_code, 204)
