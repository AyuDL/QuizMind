from apps.common.models import UuidModel, TimestampModel
from django.db import models

class Category(UuidModel):
    content = models.CharField(max_length=150, unique=True)

class Quiz(UuidModel, TimestampModel):
    title = models.CharField(max_length=150)
    description = models.TextField()
    difficulty = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
    user = models.ForeignKey("users.User", on_delete=models.PROTECT, related_name="created_quizzs")
    uploaded_file = models.ForeignKey("uploads.UploadedFile", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey("quizzs.Category", on_delete=models.SET_NULL, null=True, blank=True)

class QuizUser(UuidModel, TimestampModel):
    quiz_point = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="participation")
    quiz = models.ForeignKey("quizzs.Quiz", on_delete=models.CASCADE, related_name="participations")

    class Meta:
        unique_together = ("user", "quiz")

class Question(UuidModel):
    title = models.CharField()
    explanation = models.TextField(blank=True)
    quiz = models.ForeignKey("quizzs.Quiz", on_delete=models.CASCADE, related_name="questions")

class QuestionChoice(UuidModel):
    content = models.CharField()
    is_true = models.BooleanField(default=False)
    question = models.ForeignKey("quizzs.Question", on_delete=models.CASCADE, related_name="choices")   #related_name="choices" is for use it when call "question.choices.all()" by example