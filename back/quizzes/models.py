from django.db import models
from django.conf import settings

class Quiz(models.Model):
    question = models.TextField()
    answer = models.BooleanField()
    description = models.TextField()

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'created_at')