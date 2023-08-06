from rest_framework import serializers
from .models import AvocadoData


class AvocadoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvocadoData
        fields = [
                    'sold_plu_4046',
                    'sold_plu_4225',
                    'sold_plu_4770',
                    'small_bags',
                    'large_bags',
                    'xlarge_bags',
                    'organic',
                    'region'
                    ]