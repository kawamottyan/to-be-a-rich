from django.db import models

class PredResults(models.Model):

    one = models.FloatField()
    two = models.FloatField()
    three = models.FloatField()
    four = models.FloatField()
    five = models.FloatField()
    six = models.FloatField()
    seven = models.FloatField()
    eight = models.FloatField()
    nine = models.FloatField()
    ten = models.FloatField()
    eleven = models.FloatField()
    twelve = models.FloatField()
    thirteen = models.FloatField()
    fourteen = models.FloatField()
    fifteen = models.FloatField()
    sixteen = models.FloatField()
    seventeen = models.FloatField()
    eighteen = models.FloatField()
    #rank = models.FloatField()

    def __str__(self):
        return self.rank
