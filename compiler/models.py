#for storing submission details for this project in submission history
from django.db import models

class Submission(models.Model):
    language = models.CharField(max_length=20)
    code = models.TextField()
    user_input = models.TextField(blank=True)
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} submission at {self.created_at}"

