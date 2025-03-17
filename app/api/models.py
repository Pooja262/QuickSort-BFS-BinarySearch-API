from django.db import models

class AlgorithmLog(models.Model):
    algorithm_name = models.CharField(max_length=50)
    input_data = models.JSONField()  # Stores input as JSON
    output_data = models.JSONField()  # Stores output as JSON
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set timestamp

    def __str__(self):
        return f"{self.algorithm_name} - {self.timestamp}"

