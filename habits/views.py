from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializer import HabitSerializer
from users.permissions import IsModer, IsOwner


class HabitViewSet(ModelViewSet):
    """ViewSet для управления привычками"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        """Возвращает привычки для текущего пользователя"""
        return Habit.objects.filter(User=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.User = self.request.user
        habit.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)

        return super().get_permissions()


class PublicHabitListView(ListAPIView):
    """Generic view для списка публичных привычек"""

    queryset = Habit.objects.filter(is_published=True)
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [AllowAny]


class PublicHabitDetailView(RetrieveAPIView):
    """Generic view для детального просмотра публичной привычки"""

    queryset = Habit.objects.filter(is_published=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
