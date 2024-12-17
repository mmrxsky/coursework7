from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PublicHabitListView, PublicHabitDetailView

app_name = HabitsConfig.name

router = SimpleRouter()
router.register(r"", HabitViewSet)

urlpatterns = [
    path('public/', PublicHabitListView.as_view(), name='public-habits-list'),
    path('public/<int:pk>/', PublicHabitDetailView.as_view(), name='public-habits-detail'),
] + router.urls
