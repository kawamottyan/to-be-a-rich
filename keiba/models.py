from django.db import models

class PredResults(models.Model):

    frame_number = models.FloatField()
    horse_number = models.FloatField()
    horse_weight = models.FloatField()
    distance = models.FloatField()
    rank = models.FloatField()

    def __str__(self):
        return self.rank
