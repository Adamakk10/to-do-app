from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Task

from task.serializers import TaskSerializer


TASK_URL = reverse('tasks:task-list')


class PublicTaskTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required"""
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'test1234',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_tasks(self):
        """test retrieving tasks"""
        Task.objects.create(user=self.user, task='workout')
        Task.objects.create(user=self.user, task='shopping')

        res = self.client.get(TASK_URL)

        tasks = Task.objects.all().order_by('-task')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tasks_limited_to_user(self):
        """test that each user gets own task list"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'other1234'
        )
        Task.objects.create(user=user2, task='workout')
        task = Task.objects.create(user=self.user, task='shopping')

        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['task'], task.task)

    def test_creating_tasks(self):
        """test that we can creste tasks successfully"""
        payload = {'task': 'workout'}
        self.client.post(TASK_URL, payload)

        exists = Task.objects.filter(
            user=self.user,
            task=payload['task']
        ).exists()
        self.assertTrue(exists)

    def test_create_task_invalid(self):
        """test creating task with invalids"""
        payload = {'task': ''}
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        

