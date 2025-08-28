from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    PERIOD_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    freq_count = models.PositiveIntegerField(default=1)
    freq_period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "freq_period"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class HabitLog(models.Model):
    STATUS_CHOICES = [
        ("done", "Done"),
        ("skip", "Skip"),
    ]

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("habit", "date")
        indexes = [
            models.Index(fields=["habit", "date"]),
        ]

    def __str__(self):
        return f"{self.habit.title} - {self.date} - {self.status}"