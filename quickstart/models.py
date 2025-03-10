from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Professor(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}" if self.code else self.name
    
class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    year = models.IntegerField()
    semester = models.IntegerField()
    professors = models.ManyToManyField(Professor, related_name="modules")

    def __str__(self):
        return f"{self.name} ({self.year})"
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField(choices=[(i, i) for i in range(1, 3)])
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'professor', 'module', 'year', 'semester')  # A user can't rate the same professor for the same module twice

    def __str__(self):
        return f"{self.user.username} rated {self.professor.name} - {self.rating}/5"