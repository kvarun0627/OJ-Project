#for storing submission details for this project in submission history
from django.db import models
from django.contrib.auth.models import User
from questions.models import Question

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    verdict = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class TestCaseResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    language = models.CharField(max_length=20)
    input_data = models.TextField(blank=True)
    user_output = models.TextField(blank=True)
    expected_output = models.TextField(blank=True)
    code=models.TextField()
# question = models.ForeignKey(Question, on_delete=models.CASCADE)
# language = models.CharField(max_length=20)
# code = models.TextField()