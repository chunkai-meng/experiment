from django.db import models


# Create your models here.
class Bundle(models.Model):
    name = models.CharField(max_length=100)
    length = models.IntegerField()

    @property
    def get_length_value(self):
        print(float(self.length or 0))
        return float(self.length or 0)
