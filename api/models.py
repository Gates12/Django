from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)  # Assuming international format
    email = models.EmailField(blank=True, null=True)  # Optional email field
    spam_likelihood = models.FloatField(default=0.0)  # Probability of being spam (0.0 to 1.0)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class SpamReport(models.Model):
    reported_number = models.CharField(max_length=15)  # The number reported as spam
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    spam_count = models.IntegerField(default=1)  # Count of how many times this number has been reported
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reported_number} reported by {self.reported_by.username} on {self.created_at}"
