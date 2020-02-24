from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    location = models.CharField(max_length=100, null=False, blank=False)
    start_time = models.DateTimeField(default=timezone.now, null=False, blank=False)
    end_time = models.DateTimeField(default=timezone.now, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True, default="System")
    updated_by = models.CharField(max_length=50, null=True, blank=True, default="System")

    def __str__(self):
        return self.name


class Registration(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              limit_choices_to={'start_time__gte': timezone.now()})
    email = models.EmailField(null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True, default="System")
    updated_by = models.CharField(max_length=50, null=True, blank=True, default="System")

    class Meta:
        unique_together = ("event", "email")

    def __str__(self):
        return self.name

