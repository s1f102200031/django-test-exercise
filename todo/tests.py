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
        
    def test_index_get_order_post(self):
        task1 = Task(title='task1', due_at =timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        task2 = Task(title='task2', due_at =timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()
        client = Client()
        responce = client.get('/?order=post')
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(responce.context['tasks'][0], task2)
        self.assertEqual(responce.context['tasks'][1], task1)
        
    def test_index_get_order_due(self):
        task1 = Task(title='task1', due_at =timezone.make_aware(datetime(2024, 7, 1)))
        task1.save()
        task2 = Task(title='task2', due_at =timezone.make_aware(datetime(2024, 8, 1)))
        task2.save()
        client = Client()
        responce = client.get('/?order=due')
        
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.templates[0].name, 'todo/index.html')
        self.assertEqual(responce.context['tasks'][0], task1)
        self.assertEqual(responce.context['tasks'][1], task2)
        
    
    def test_detail_get_success(self):
        task= Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task.save()
        client = Client()
        response = client.get('/{}/'.format(task.pk))
        
        self.assertEqual (response.status_code, 200)
        self.assertEqual (response.templates[0].name, 'todo/detail.html')
        self.assertEqual (response.context['task'], task)
        
    def test_detail_get_fail(self):
        client = Client()
        response = client.get('/1/')
        
        self.assertEqual(response.status_code, 404)