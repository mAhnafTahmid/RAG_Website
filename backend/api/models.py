from django.db import models
from django.contrib.auth.models import User


class QA(models.Model):
    ai = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="QA")

    def __str__(self):
        return f"QA from {self.user.username}"
