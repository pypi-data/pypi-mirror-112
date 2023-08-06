from django.db import models


class AvocadoData(models.Model):
    observation_date = models.DateTimeField()
    # features
    sold_plu_4046 = models.IntegerField()
    sold_plu_4225 = models.IntegerField()
    sold_plu_4770 = models.IntegerField()
    small_bags = models.IntegerField()
    large_bags = models.IntegerField()
    xlarge_bags = models.IntegerField()
    organic = models.BooleanField()
    region = models.CharField(max_length=50)
    # gold data
    actual_average_price = models.FloatField()


class AvocadoPricePrediction(models.Model):
    avocado_data = models.ForeignKey(AvocadoData, on_delete=models.CASCADE)
    predicted_average_price = models.FloatField()
    prediction_date = models.DateTimeField()
