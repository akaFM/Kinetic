from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from .views import index, get_day_tasks_description_json, login, complete_task
from .models import Task
import json
import uuid
from django.utils import timezone
from .models import TaskType


User = get_user_model()


# SETUP:

class TestSetup(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="username_test", password="Testpassw0rd!")

        # Create a mock task for testing:
        self.testing_task_1 = Task.objects.create(
            id                = uuid.uuid4(), 
            user              = self.user,
            name              = "Test Task 1",
            due_date          = timezone.datetime(2025, 2, 27),
            created_at        = timezone.datetime(2025, 2, 26),  
            completed         = False,
            description       = "Test Task 1 description",
            type              = TaskType.GENERAL,
            urgency           = 5,
            recurring_pattern = None 
        )
    
    # Helper functions:
    def assertTask(self, tasks, comparee_task):
        test_task = tasks[0]
        self.assertEqual(test_task['id'],          str(comparee_task.id))
        self.assertEqual(test_task['name'],        comparee_task.name)
        self.assertEqual(test_task['description'], comparee_task.description)
        self.assertEqual(test_task['type'],        comparee_task.type)
        self.assertEqual(test_task['urgency'],     comparee_task.urgency)
        self.assertEqual(test_task['completed'],   comparee_task.completed)






# --------- UNIT TESTS ---------



# State-based unit tests:

class GetDayTasksDescriptionJsonStateUnitTests(TestSetup):
    def test_get_day_tasks_description_json_state(self):
        # ARRANGE PHASE:
        # Create a mock request AND assign it to a mock user for testing:
        request      = self.factory.get(reverse('get_day_tasks_description_json', args=[2025, 2, 27]))
        request.user = self.user

        # ACT PHASE:
        # Test get_day_tasks_description_json() by calling it and then storing its response...
        # ...(fyi: response is a JsonResponse. By default, it returns a status code and content which is an array of tasks):
        response    = get_day_tasks_description_json(request, 2025, 2, 27)

        # Get status code AND content (a tasks array) for assert phase:
        status_code = response.status_code
        content     = json.loads(response.content)
        tasks       = content['tasks']

        # ASSERT PHASE:
        # Check that response status code is successful when calling get_day_tasks_description_json() (a status code of 200 means success):
        self.assertEqual(status_code, 200)

        # Check that repsonse content is as expected (ie., check that it matches mock testing_task_1):
        self.assertTask(tasks, self.testing_task_1)



# Interaction-based unit tests:

class TaskModelInteractionUnitTests(TestSetup):
    def test_task_model_properties_interactions(self):
        # ARRANGE:
        test_task_1 = self.testing_task_1

        # ACT:
        test_description = test_task_1.get_description
        test_type        = test_task_1.get_type
        test_urgency     = test_task_1.get_urgency

        # ASSERT:
        self.assertEqual(test_description, self.testing_task_1.description)
        self.assertEqual(test_type, self.testing_task_1.type)
        self.assertEqual(test_urgency, self.testing_task_1.urgency)






# --------- INTEGRATION TESTS ---------



class GetDayTasksDescriptionJsonIntegrationTests(TestSetup):
    def test_get_day_tasks_description_json_integration(self):
        # The client() makes it integration. 

        # ARRANGE PHASE:
        # It logs in to check that get_day_tasks_description_json() only works when a user is logged in.
        # That is, ensure integration between get_day_tasks_description_json() and login().
        self.client.login(username='username_test', password='Testpassw0rd!')

        # ACT PHASE:
        # Test the full get request cycle. That is, integration between database, view, response and stuff:
        response = self.client.get(reverse('get_day_tasks_description_json', args=[2025, 2, 27]))

        # Get status code AND content (a tasks array) for assert phase:
        status_code = response.status_code
        content     = json.loads(response.content)
        tasks       = content['tasks']

        # ASSERT PHASE:
        # Check that response status code is successful when calling get_day_tasks_description_json() (a status code of 200 means success):
        self.assertEqual(status_code, 200)

        # Check that repsonse content is as expected (ie., check that it matches mock testing_task_1):
        self.assertTask(tasks, self.testing_task_1)