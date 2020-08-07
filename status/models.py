from django.db import models

class StateData(models.Model):
    location = models.CharField(max_length=128)
    confirmed = models.BigIntegerField()
    confirmed_today = models.BigIntegerField()
    active = models.BigIntegerField()
    active_today = models.BigIntegerField()
    recovered = models.BigIntegerField()
    recovered_today = models.BigIntegerField()
    deaths = models.BigIntegerField()
    deaths_today = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Data of {self.location} at {self.timestamp}"

    class Meta:
        ordering = ['-active','-timestamp']
        verbose_name = "States Data"
        verbose_name_plural = "States Data"


   
