from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PublicHabitViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register(r"", HabitViewSet)
router.register(r"public", PublicHabitViewSet, basename="public-habits")

urlpatterns = [] + router.urls
