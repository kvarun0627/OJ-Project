from django.db import models

class Question(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField()
    constraints=models.TextField()
    tags=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    testcases=models.JSONField()
    
    def get_constraints_list(self):
        return [c.strip() for c in self.constraints.splitlines() if c.strip()]

    def get_question(self):
        return [c.strip() for c in self.description.splitlines() if c.strip()]

