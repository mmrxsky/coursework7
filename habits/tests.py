from datetime import datetime, time
from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from habits.serializer import HabitSerializer

User = get_user_model()

class HabitTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных для тестирования."""
        self.client = APIClient()
        
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123',
            tg_chat_id='123456789'
        )
        
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)
        
        # Создаем тестовую привычку
        self.habit_data = {
            'user': self.user,
            'place': 'Дом',
            'time': time(hour=8, minute=0),
            'action': 'Тестовая привычка',
            'periodicity': 1,
            'is_published': True
        }
        self.habit = Habit.objects.create(**self.habit_data)

    def test_create_habit(self):
        """Тест создания привычки."""
        data = {
            'place': 'Офис',
            'time': '09:00',
            'action': 'Новая привычка',
            'periodicity': 2
        }
        response = self.client.post('/habits/', data=data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(response.data['action'], 'Новая привычка')
        
    def test_list_habits(self):
        """Тест получения списка привычек пользователя."""
        response = self.client.get('/habits/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_retrieve_habit(self):
        """Тест получения деталей привычки."""
        response = self.client.get(f'/habits/{self.habit.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], self.habit_data['action'])
        
    def test_update_habit(self):
        """Тест обновления привычки."""
        data = {'action': 'Обновленная привычка'}
        response = self.client.patch(f'/habits/{self.habit.id}/', data=data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Обновленная привычка')
        
    def test_delete_habit(self):
        """Тест удаления привычки."""
        response = self.client.delete(f'/habits/{self.habit.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
        
    def test_list_public_habits(self):
        """Тест получения списка публичных привычек."""
        response = self.client.get('/habits/public/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_habit_validation(self):
        """Тест валидации данных привычки."""
        # Тест на некорректную периодичность
        data = {
            'action': 'Тест',
            'periodicity': 8  # Некорректная периодичность
        }
        response = self.client.post('/habits/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Тест на время выполнения
        data = {
            'action': 'Тест',
            'time_to_complete': '02:00'  # Слишком долгое время выполнения
        }
        response = self.client.post('/habits/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class HabitNotificationTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных для тестирования уведомлений."""
        self.user = User.objects.create_user(
            email='test@test.com',
            password='test123',
            tg_chat_id='123456789'
        )
        
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time=time(hour=8, minute=0),
            action='Тестовая привычка',
            periodicity=1
        )
    
    @patch('habits.services.send_telegram_message')
    def test_send_notification(self, mock_send_message):
        """Тест отправки уведомлений."""
        from habits.tasks import send_notifications
        
        # Устанавливаем текущее время
        current_time = datetime.now().replace(hour=8, minute=0)
        
        with patch('django.utils.timezone.now', return_value=current_time):
            # Запускаем задачу
            send_notifications()
            
            # Проверяем, что уведомление было отправлено
            mock_send_message.assert_called_once()
            
            # Проверяем аргументы вызова
            args = mock_send_message.call_args[0]
            self.assertEqual(args[0], '123456789')  # chat_id
            self.assertIn('Тестовая привычка', args[1])  # message
            
    def test_notification_periodicity(self):
        """Тест периодичности уведомлений."""
        from habits.tasks import send_notifications
        
        # Устанавливаем периодичность 2 дня
        self.habit.periodicity = 2
        self.habit.save()
        
        # Первое уведомление
        current_time = datetime.now().replace(hour=8, minute=0)
        with patch('django.utils.timezone.now', return_value=current_time):
            with patch('habits.services.send_telegram_message') as mock_send:
                send_notifications()
                self.assertTrue(mock_send.called)
        
        # Проверяем, что на следующий день уведомление не отправляется
        next_day = current_time.replace(day=current_time.day + 1)
        with patch('django.utils.timezone.now', return_value=next_day):
            with patch('habits.services.send_telegram_message') as mock_send:
                send_notifications()
                self.assertFalse(mock_send.called)