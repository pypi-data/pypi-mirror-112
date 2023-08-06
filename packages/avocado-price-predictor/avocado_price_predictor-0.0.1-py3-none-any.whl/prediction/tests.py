import pytest
from django.urls import reverse
from http import HTTPStatus
from json import dumps, loads


@pytest.fixture
def data():
    return {
        'sold_plu_4046' : 5,
        'sold_plu_4225' : 6,
        'sold_plu_4770': 8,
        'small_bags': 4,
        'large_bags': 0,
        'xlarge_bags': 0,
        'organic': True,
        'region': 'Albany'
    }

def test_price_prediction_method_not_allowed(client):
    response = client.get(reverse('predict'))
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

def test_price_prediction_empty(client):
    data = dict()
    
    response = client.post(reverse('predict'), dumps(data).encode('utf-8'), content_type="application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_price_prediction_invalid_data(client, data):
    data['sold_plu_4046'] = 'not number'

    response = client.post(reverse('predict'), dumps(data).encode('utf-8'), content_type="application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_price_prediction_missing_field(client, data):
    del data['sold_plu_4046']

    response = client.post(reverse('predict'), dumps(data).encode('utf-8'), content_type="application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_price_prediction_valid(client, data):
    response = client.post(reverse('predict'), dumps(data).encode('utf-8'), content_type="application/json")
    assert response.status_code == HTTPStatus.OK

    content = loads(response.content.decode('utf-8'))
    assert 'predicted_average_price' in content.keys()
   
def test_default_method_not_allowed(client):
    response = client.post(reverse('default'))
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

def test_default_valid(client, data):
    response = client.get(reverse('default'))
    assert response.status_code == HTTPStatus.OK

    content = loads(response.content.decode('utf-8'))
    assert data.keys() == content.keys()
    assert all(len(v) == 0 for v in content.values())