from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from todo.models import Task

# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample1(self):
        self.assertEqual(1 + 2, 3)

# 動作確認テストの追加
class TaskModelTestCase(TestCase):
    def test_cerate_task1(self): #締切有り
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()
        
        self.assertFalse(task.is_overdue(current))
        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task1')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)
        
    def test_cerate_task2(self): #締切無し
        task = Task(title='task2')
        task.save()
        
        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task2')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, None)
        
        
class TodoViewTestCase(TestCase):
    def test_index_get(self):
        client = Client()
        responce = client.get('/')
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(len(responce.context['tasks']), 0)
        
    def test_index_post(self):
        client = Client()
        data = {'title':'Test Task', 'due_at':'2024-06-30 23:59:59'}
        responce = client.post('/', data)
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(len(responce.context['tasks']), 1)
        