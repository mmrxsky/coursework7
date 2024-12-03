from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit


class HabitsTestCase(APITestCase):
    def setUp(self):
        pass

    def test_create_habit(self):
        """Тестирование создания привычки."""
        data = {"action": "Test", "periodicity": 2}
        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "action": "Test",
                "periodicity": 2,
                "associted_habit": None,
                "is_published": None,
                "nice_habit": None,
                "place": None,
                "reward": None,
                "time": None,
                "time_to_complete": None,
                "user": None,
            },
        )

        self.assertTrue(Habit.objects.all().exists())

    def test_list_habits(self):
        """Тестирование вывода списка привычек."""

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(), {"count": 0, "next": None, "previous": None, "results": []}
        )
