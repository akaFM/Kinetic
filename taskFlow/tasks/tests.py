import json
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import JsonResponse
from django.urls import reverse 
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from datetime import date, timedelta

from .models import Task, TaskType, RecurringPattern, User
from .views import get_today, filter_tasks_by_category, group_tasks_by_day, validate_password, create_recurring_tasks, get_next_date, get_day_tasks_description_json, index, login, logout, create_task, complete_task, uncomplete_task, edit_tasks
from .forms import TaskForm

class GetTodayTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_today_with_valid_date(self):
        request = self.factory.post('/', {'date': '2025-12-25'})
        result = get_today(request)
        expected = date(2025, 12, 25)
        self.assertEqual(result, expected)

    def test_get_today_with_invalid_date(self):
        request = self.factory.post('/', {'date': 'invalid-date'})
        result = get_today(request)
        self.assertEqual(result, date.today())

    def test_get_today_with_no_date(self):
        request = self.factory.post('/', {})
        result = get_today(request)
        self.assertEqual(result, date.today())


class FilterTasksByCategoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        today = date.today()
        cls.task1 = Task.objects.create(
            name="Task 1",
            type=TaskType.WORK,
            user=cls.user,
            due_date=today
        )
        cls.task2 = Task.objects.create(
            name="Task 2", 
            type=TaskType.FUN,
            user=cls.user,
            due_date=today
        )
        
        cls.pattern1 = RecurringPattern.objects.create(
            name="Work Pattern",
            type=TaskType.WORK,
            user=cls.user,
            repetition_period=RecurringPattern.RepetitionPeriod.DAILY,
            start_date=today,
            end_date=today
        )
        cls.pattern2 = RecurringPattern.objects.create(
            name="Fun Pattern",
            type=TaskType.FUN,
            user=cls.user,
            repetition_period=RecurringPattern.RepetitionPeriod.DAILY,
            start_date=today,
            end_date=today
        )
        
        cls.recurring_task1 = Task.objects.create(
            name="Recurring Task 1",
            user=cls.user,
            recurring_pattern=cls.pattern1,
            due_date=today
        )
        cls.recurring_task2 = Task.objects.create(
            name="Recurring Task 2",
            user=cls.user,
            recurring_pattern=cls.pattern2,
            due_date=today
        )

    def test_filter_work_tasks(self):
        today = date.today()
        tasks = Task.objects.all()
        filtered = filter_tasks_by_category(tasks, TaskType.WORK, today.year, today.month, today.day)
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.task1, filtered)
        self.assertIn(self.recurring_task1, filtered)

    def test_filter_fun_tasks(self):
        today = date.today()
        tasks = Task.objects.all()
        filtered = filter_tasks_by_category(tasks, TaskType.FUN, today.year, today.month, today.day)
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.task2, filtered)
        self.assertIn(self.recurring_task2, filtered)

    def test_filter_invalid_category(self):
        today = date.today()
        tasks = Task.objects.all()
        filtered = filter_tasks_by_category(tasks, "INVALID", today.year, today.month, today.day)
        self.assertEqual(filtered, tasks)

    def test_filter_none_category(self):
        today = date.today()
        tasks = Task.objects.all()
        filtered = filter_tasks_by_category(tasks, None, today.year, today.month, today.day)
        self.assertEqual(filtered, tasks)


class GroupTasksByDayTests(TestCase):
    @classmethod 
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        cls.task1 = Task.objects.create(
            name="Task 1",
            user=cls.user,
            due_date=date(2025, 12, 1)
        )
        cls.task2 = Task.objects.create(
            name="Task 2",
            user=cls.user, 
            due_date=date(2025, 12, 1)
        )
        cls.task3 = Task.objects.create(
            name="Task 3",
            user=cls.user,
            due_date=date(2025, 12, 15)
        )

    def test_group_tasks_december_2025(self):
        tasks = Task.objects.all()
        grouped = group_tasks_by_day(tasks, 2025, 12)
        
        self.assertEqual(len(grouped), 31)
        
        self.assertEqual(len(grouped[0]), 2)
        self.assertIn(self.task1, grouped[0])
        self.assertIn(self.task2, grouped[0])
        
        self.assertEqual(len(grouped[14]), 1)
        self.assertIn(self.task3, grouped[14])
        
        self.assertEqual(len(grouped[2]), 0)
        self.assertEqual(len(grouped[30]), 0)

    def test_group_tasks_empty_month(self):
        tasks = Task.objects.none()
        grouped = group_tasks_by_day(tasks, 2025, 2)
        
        self.assertEqual(len(grouped), 28)
        for day in grouped:
            self.assertEqual(len(day), 0)


class ValidatePasswordTests(TestCase):
    def test_validate_password_valid(self):
        self.assertTrue(validate_password("Pass1!word"))
        self.assertTrue(validate_password("H3llo@World"))
        self.assertTrue(validate_password("Abcd12#$"))

    def test_validate_password_too_short(self):
        self.assertFalse(validate_password("Pa1!"))

    def test_validate_password_too_long(self):
        self.assertFalse(validate_password("Password123!@#$%^&*()" * 2))

    def test_validate_password_no_uppercase(self):
        self.assertFalse(validate_password("pass123!"))

    def test_validate_password_no_lowercase(self):
        self.assertFalse(validate_password("PASS123!"))

    def test_validate_password_no_number(self):
        self.assertFalse(validate_password("Password!"))

    def test_validate_password_no_special_char(self):
        self.assertFalse(validate_password("Password123"))


class CreateRecurringTasksTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_daily_recurring_tasks(self):
        pattern = RecurringPattern.objects.create(
            name="Daily Task",
            user=self.user,
            repetition_period=RecurringPattern.RepetitionPeriod.DAILY,
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 5)
        )
        
        create_recurring_tasks(self.user, pattern)
        
        tasks = Task.objects.filter(recurring_pattern=pattern)
        self.assertEqual(tasks.count(), 5)
        
        expected_dates = [
            date(2025, 12, 1),
            date(2025, 12, 2),
            date(2025, 12, 3),
            date(2025, 12, 4),
            date(2025, 12, 5)
        ]
        
        for task, expected_date in zip(tasks, expected_dates):
            self.assertEqual(task.due_date, expected_date)
            self.assertEqual(task.name, pattern.name)
            self.assertEqual(task.user, self.user)

    def test_create_weekly_recurring_tasks(self):
        pattern = RecurringPattern.objects.create(
            name="Weekly Task",
            user=self.user,
            repetition_period=RecurringPattern.RepetitionPeriod.WEEKLY,
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 22)
        )
        
        create_recurring_tasks(self.user, pattern)
        
        tasks = Task.objects.filter(recurring_pattern=pattern)
        self.assertEqual(tasks.count(), 4)
        
        expected_dates = [
            date(2025, 12, 1),
            date(2025, 12, 8),
            date(2025, 12, 15),
            date(2025, 12, 22)
        ]
        
        for task, expected_date in zip(tasks, expected_dates):
            self.assertEqual(task.due_date, expected_date)
            self.assertEqual(task.name, pattern.name)
            self.assertEqual(task.user, self.user)

    def test_create_monthly_recurring_tasks(self):
        pattern = RecurringPattern.objects.create(
            name="Monthly Task",
            user=self.user,
            repetition_period=RecurringPattern.RepetitionPeriod.MONTHLY,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 3, 1)
        )
        
        create_recurring_tasks(self.user, pattern)
        
        tasks = Task.objects.filter(recurring_pattern=pattern)
        self.assertEqual(tasks.count(), 3)
        
        expected_dates = [
            date(2025, 1, 1),
            date(2025, 2, 1),
            date(2025, 3, 1)
        ]
        
        for task, expected_date in zip(tasks, expected_dates):
            self.assertEqual(task.due_date, expected_date)
            self.assertEqual(task.name, pattern.name)
            self.assertEqual(task.user, self.user)

    def test_create_recurring_tasks_same_start_end_date(self):
        pattern = RecurringPattern.objects.create(
            name="Single Day Task",
            user=self.user,
            repetition_period=RecurringPattern.RepetitionPeriod.DAILY,
            start_date=date(2025, 12, 1),
            end_date=date(2025, 12, 1)
        )
        
        create_recurring_tasks(self.user, pattern)
        
        tasks = Task.objects.filter(recurring_pattern=pattern)
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks[0].due_date, date(2025, 12, 1))


class GetNextDateTests(TestCase):
    def test_get_next_date_daily(self):
        current_date = date(2025, 12, 1)
        next_date = get_next_date(current_date, RecurringPattern.RepetitionPeriod.DAILY)
        self.assertEqual(next_date, date(2025, 12, 2))

    def test_get_next_date_weekly(self):
        current_date = date(2025, 12, 1)
        next_date = get_next_date(current_date, RecurringPattern.RepetitionPeriod.WEEKLY)
        self.assertEqual(next_date, date(2025, 12, 8))

    def test_get_next_date_monthly_same_year(self):
        current_date = date(2025, 11, 1)
        next_date = get_next_date(current_date, RecurringPattern.RepetitionPeriod.MONTHLY)
        self.assertEqual(next_date, date(2025, 12, 1))

    def test_get_next_date_monthly_next_year(self):
        current_date = date(2025, 12, 1)
        next_date = get_next_date(current_date, RecurringPattern.RepetitionPeriod.MONTHLY)
        self.assertEqual(next_date, date(2026, 1, 1))

    def test_get_next_date_yearly(self):
        current_date = date(2025, 12, 1)
        next_date = get_next_date(current_date, RecurringPattern.RepetitionPeriod.YEARLY)
        self.assertEqual(next_date, date(2026, 12, 1))

    def test_get_next_date_invalid_period(self):
        current_date = date(2025, 12, 1)
        next_date = get_next_date(current_date, 'INVALID')
        self.assertEqual(next_date, current_date)


class GetDayTasksDescriptionJsonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
        cls.factory = RequestFactory()

        cls.task1 = Task.objects.create(
            name="Task 1",
            description="Description 1",
            user=cls.user,
            due_date=date(2025, 12, 1)
        )
        cls.task2 = Task.objects.create(
            name="Task 2",
            description="Description 2", 
            user=cls.user,
            due_date=date(2025, 12, 1)
        )
        cls.task3 = Task.objects.create(
            name="Task 3",
            description="Description 3",
            user=cls.user,
            due_date=date(2025, 12, 15)
        )

    def test_get_day_tasks_description_json_multiple_tasks(self):
        request = self.factory.get('/')
        request.user = self.user
        
        response = get_day_tasks_description_json(request, 2025, 12, 1)
        
        self.assertIsInstance(response, JsonResponse)
        data = json.loads(response.content)
        
        self.assertEqual(len(data['tasks']), 2)
        tasks = sorted(data['tasks'], key=lambda x: x['name'])
        self.assertEqual(tasks[0]['name'], 'Task 1')
        self.assertEqual(tasks[0]['description'], 'Description 1')
        self.assertEqual(tasks[1]['name'], 'Task 2')
        self.assertEqual(tasks[1]['description'], 'Description 2')

    def test_get_day_tasks_description_json_single_task(self):
        request = self.factory.get('/')
        request.user = self.user
        
        response = get_day_tasks_description_json(request, 2025, 12, 15)
        
        self.assertIsInstance(response, JsonResponse)
        data = json.loads(response.content)
        
        self.assertEqual(len(data['tasks']), 1)
        self.assertEqual(data['tasks'][0]['name'], 'Task 3')
        self.assertEqual(data['tasks'][0]['description'], 'Description 3')

    def test_get_day_tasks_description_json_no_tasks(self):
        request = self.factory.get('/')
        request.user = self.user
        
        response = get_day_tasks_description_json(request, 2025, 12, 25)
        
        self.assertIsInstance(response, JsonResponse)
        data = json.loads(response.content)
        
        self.assertEqual(len(data['tasks']), 0)


class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='12345')
        
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_requires_login(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login?next=/')

    def test_index_view_renders_dashboard_template(self):
        request = self.factory.get('/')
        request.user = self.user
        request.POST = {}
        
        response = index(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


class LoginViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='Test123!')

    def test_existing_user_wrong_password(self):
        request = self.factory.post('/', {
            'username': 'testuser',
            'password': 'WrongPass123!'  
        })

        response = login(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incorrect password")

    def test_new_user_invalid_password(self):
        request = self.factory.post('/', {
            'username': 'newuser', 
            'password': 'weak'
        })

        response = login(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password must be")
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_get_request_logged_out(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        response = login(request)
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Enter your login credentials")

    def test_get_request_logged_in(self):
        request = self.factory.get('/')
        request.user = self.user

        response = login(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))


class LogoutViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_logout_redirects_to_index(self):
        request = self.factory.get('/logout')
        request.user = self.user
        middleware = SessionMiddleware(get_response=lambda req: None)
        middleware.process_request(request)
        request.session.save()
        response = logout(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_logout_anonymous_user(self):
        request = self.factory.get('/logout') 
        request.user = AnonymousUser()
        middleware = SessionMiddleware(get_response=lambda req: None)
        middleware.process_request(request)
        request.session.save()
        response = logout(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertEqual(response.url, reverse('index'))


class CreateTaskTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.today = timezone.now().date()

    def test_create_single_task(self):
        request = self.factory.post(reverse('create_task'), {
            'name': 'Test Task',
            'description': 'Test Description',
            'type': TaskType.WORK,
            'urgency': 1,
            'due_date': self.today,
            'is_recurring': False
        })
        request.user = self.user

        response = create_task(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        
        task = Task.objects.get(name='Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.type, TaskType.WORK)
        self.assertEqual(task.urgency, 1)
        self.assertEqual(task.due_date, self.today)
        self.assertEqual(task.user, self.user)
        self.assertIsNone(task.recurring_pattern)

    def test_create_recurring_task(self):
        request = self.factory.post(reverse('create_task'), {
            'name': 'Recurring Task',
            'description': 'Recurring Description',
            'type': TaskType.WORK,
            'urgency': 2,
            'is_recurring': True,
            'start_date': self.today,
            'end_date': self.today + timedelta(days=10),
            'repetition_period': RecurringPattern.RepetitionPeriod.DAILY
        })
        request.user = self.user

        response = create_task(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

        pattern = RecurringPattern.objects.get(name='Recurring Task')
        self.assertEqual(pattern.description, 'Recurring Description')
        self.assertEqual(pattern.type, TaskType.WORK) 
        self.assertEqual(pattern.urgency, 2)
        self.assertEqual(pattern.start_date, self.today)
        self.assertEqual(pattern.end_date, self.today + timedelta(days=10))
        self.assertEqual(pattern.user, self.user)

        tasks = Task.objects.filter(recurring_pattern=pattern)
        self.assertEqual(tasks.count(), 11)
        for task in tasks:
            self.assertEqual(task.name, 'Recurring Task')
            self.assertEqual(task.type, 'General')
            self.assertEqual(task.user, self.user)

    def test_create_recurring_task_capped_at_5_years(self):
        request = self.factory.post(reverse('create_task'), {
            'name': 'Long Recurring Task',
            'description': 'Long Description',
            'type': TaskType.WORK,
            'urgency': 1,
            'is_recurring': True,
            'start_date': self.today,
            'end_date': self.today + timedelta(days=2000),
            'repetition_period': RecurringPattern.RepetitionPeriod.DAILY
        })
        request.user = self.user

        response = create_task(request)

        pattern = RecurringPattern.objects.get(name='Long Recurring Task')
        self.assertEqual(pattern.end_date, self.today + timedelta(days=5*365))

    def test_get_create_task_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_task'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)


class CompleteTaskTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(
            name="Test Task",
            user=self.user,
            completed=False
        )

    def test_complete_task_successful(self):
        request = self.factory.post('/complete_task',
            data=json.dumps({'task_id': str(self.task.id)}),
            content_type='application/json')
        request.user = self.user
        
        response = complete_task(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_complete_task_not_found(self):
        request = self.factory.post('/complete_task',
            data=json.dumps({'task_id': 99999}),
            content_type='application/json')
        request.user = self.user
        
        response = complete_task(request)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), 
            {'status': 'error', 'message': 'Task not found'})

    def test_complete_task_wrong_method(self):
        request = self.factory.get('/complete_task')
        request.user = self.user
        
        response = complete_task(request)
        
        self.assertEqual(response.status_code, 405)
        self.assertEqual(json.loads(response.content),
            {'status': 'error', 'message': 'Invalid method'})
        

class UncompleteTaskTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(
            name="Test Task",
            user=self.user,
            completed=True  
        )

    def test_uncomplete_task_successful(self):
        request = self.factory.post(
            '/uncomplete_task',
            data=json.dumps({'task_id': str(self.task.id)}),
            content_type='application/json'
        )
        request.user = self.user
        
        response = uncomplete_task(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)  

    def test_uncomplete_task_not_found(self):
        request = self.factory.post(
            '/uncomplete_task',
            data=json.dumps({'task_id': 99999}),
            content_type='application/json'
        )
        request.user = self.user
        
        response = uncomplete_task(request)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content),
            {'status': 'error', 'message': 'Task not found'}
        )

    def test_uncomplete_task_wrong_method(self):
        request = self.factory.get('/uncomplete_task')
        request.user = self.user
        
        response = uncomplete_task(request)
        
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content),
            {'status': 'error', 'message': 'Invalid method'}
        )


class EditTasksTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        self.one_time_task = Task.objects.create(
            name="One-Time Task",
            user=self.user,
            due_date=timezone.now().date() + timedelta(days=1),
            type=TaskType.GENERAL, 
            urgency=5
        )
        
        self.recurring_pattern = RecurringPattern.objects.create(
            name="Recurring Pattern",
            user=self.user,
            type=TaskType.WORK,  
            urgency=3,
            repetition_period=RecurringPattern.RepetitionPeriod.WEEKLY,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30)
        )
        
        self.recurring_task = Task.objects.create(
            name="Recurring Task",
            user=self.user,
            recurring_pattern=self.recurring_pattern,
            due_date=timezone.now().date() + timedelta(days=7),
            urgency=3  
        )

    def test_edit_one_time_task_success(self):
        data = {
            'task_id': self.one_time_task.id,
            'is_recurring': 'false',
            'action': 'false',
            'name': 'Updated Task',
            'type': TaskType.SCHOOL.value,  
            'urgency': '8',
            'due_date': '2024-12-31'
        }
        request = self.factory.post(reverse('edit_tasks'), data)
        request.user = self.user
        
        response = edit_tasks(request)
        
        self.assertEqual(response.status_code, 302)
        self.one_time_task.refresh_from_db()
        self.assertEqual(self.one_time_task.name, 'Updated Task')
        self.assertEqual(self.one_time_task.type, TaskType.SCHOOL.value)

    def test_edit_recurring_pattern_success(self):
        data = {
            'task_id': self.recurring_pattern.id,
            'is_recurring': 'true',
            'action': 'false',
            'name': 'Updated Pattern',
            'type': TaskType.CHORE.value,  
            'urgency': '5'
        }
        request = self.factory.post(reverse('edit_tasks'), data)
        request.user = self.user
        
        response = edit_tasks(request)
        
        self.assertEqual(response.status_code, 302)
        self.recurring_pattern.refresh_from_db()
        self.assertEqual(self.recurring_pattern.name, 'Updated Pattern')
        self.assertEqual(self.recurring_pattern.type, TaskType.CHORE.value)