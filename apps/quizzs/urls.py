from .views import QuizViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'quizzes', QuizViewSet)
urlpatterns = router.urls