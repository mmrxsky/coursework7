from datetime import datetime, timedelta

import pytz
from celery import shared_task
from django.conf import settings

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task(name="habits.tasks.send_notifications")
def send_notifications():
    """
    Периодическая задача для проверки и отправки уведомлений о привычках в telegram канал.
    Проверяет привычки и отправляет уведомления с учетом времени и периодичности выполнения.
    """
    try:
        # Получаем текущее время в нужном часовом поясе
        timezone = pytz.timezone(settings.TIME_ZONE)
        current_time = datetime.now(timezone)

        # Получаем привычки, для которых подходит время уведомления
        habits = Habit.objects.filter(
            time__hour=current_time.hour, time__minute=current_time.minute
        )

        for habit in habits:
            try:
                # Проверяем наличие пользователя и его telegram chat id
                if not habit.user or not habit.user.tg_chat_id:
                    continue

                # Проверяем периодичность
                if habit.periodicity > 1:
                    # Получаем дату последнего уведомления
                    last_notification = habit.last_notification
                    if last_notification:
                        # Проверяем, прошло ли нужное количество дней
                        days_since_last = (current_time.date() - last_notification).days
                        if days_since_last < habit.periodicity:
                            continue

                # Формируем сообщение для отправки
                message = _format_habit_message(habit)

                # Отправляем уведомление
                send_telegram_message(habit.user.tg_chat_id, message)

                # Обновляем дату последнего уведомления
                habit.last_notification = current_time.date()
                habit.save(update_fields=["last_notification"])

            except Exception as e:
                print(f"Ошибка при обработке привычки {habit.id}: {str(e)}")
                continue

    except Exception as e:
        print(f"Ошибка в задаче отправки уведомлений: {str(e)}")


def _format_habit_message(habit):
    """Форматирует сообщение для отправки в Telegram."""
    message = (
        f"🔔 Напоминание о привычке!\n\n"
        f"📝 Действие: {habit.action}\n"
        f"📍 Место: {habit.place}\n"
        f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
        f"🔄 Периодичность: {habit.periodicity} "
        f"{'день' if habit.periodicity == 1 else 'дня' if 2 <= habit.periodicity <= 4 else 'дней'}"
    )

    if habit.reward:
        message += f"\n🎁 Награда: {habit.reward}"

    if habit.time_to_complete:
        message += (
            f"\n⏱ Время на выполнение: {habit.time_to_complete.strftime('%H:%M')}"
        )

    if hasattr(habit, "associated_habit") and habit.associated_habit:
        message += f"\n🔄 Связанная привычка: {habit.associated_habit.action}"

    return message
