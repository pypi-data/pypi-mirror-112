from json import loads
from datetime import datetime
from os import environ
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from .forms import AvocadoDataForm
from .serializers import AvocadoDataSerializer
import avocado_price_predictor_model.load_model as model_loader
import avocado_price_predictor_model.predict as predictor
from avocado_price_predictor_model.preprocess import DATE_FORMAT


model = model_loader.load_model(environ['MODEL_URL'])

@require_http_methods(["POST"])
def predict(request):
    form = AvocadoDataForm(loads(request.body.decode("utf-8")))
    if not form.is_valid():
        return HttpResponseBadRequest()

    serializer = AvocadoDataSerializer(data=form.cleaned_data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()

    data = dict(serializer.data)
    data['date'] = datetime.now().strftime(DATE_FORMAT)

    prediction = predictor.predict(model, data)

    return JsonResponse({'predicted_average_price': prediction})


@require_http_methods(["GET"])
def default(request):
    return JsonResponse({f: "" for f in AvocadoDataForm.Meta.fields})