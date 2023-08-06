from django.forms import ModelForm
from .models import AvocadoData 


class AvocadoDataForm(ModelForm):
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