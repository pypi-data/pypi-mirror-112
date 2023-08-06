import pytest
from typing import Optional
import pandas as pd
from sklearn import pipeline as sk_pipeline
import avocado_price_predictor_model.load_model as model_loader
import avocado_price_predictor_model.load_data as loader
import avocado_price_predictor_model.predict as predictor


@pytest.fixture
def data():
    return {
        'sold_plu_4046': 5,
        'sold_plu_4225': 6,
        'sold_plu_4770': 8,
        'small_bags': 4,
        'large_bags': 0,
        'xlarge_bags': 0,
        'organic': True,
        'region': 'Albany',
        'date': '2020-12-27'
    }


# do not use @pytest.fixture, download once
model: Optional[sk_pipeline.Pipeline] = None


def _ensure_model():
    global model

    if not model:
        model = model_loader.load_model('https://drive.google.com/uc?id=1UiH6y3kvlWcGTpH9AV9qsQrjJZ-X9f2s')


def test_load_model_ok():
    _ensure_model()
    assert isinstance(model, sk_pipeline.Pipeline)


def test_load_model_not_found():
    none_model = model_loader.load_model('https://drive.google.com/uc?id=#111')
    assert none_model is None


def test_create_data_frame(data):
    x = loader.create_avocado_data_frame(data)
    assert x is not None
    assert isinstance(x, pd.DataFrame)
    assert len(x.columns) == len(data)


def test_prediction_ok(data):
    _ensure_model()
    y = predictor.predict(model, data)
    assert isinstance(y, float)


def test_create_data_frame_empty_data():
    x = loader.create_avocado_data_frame({})
    assert x is None


def test_prediction_empty_data():
    _ensure_model()
    y = predictor.predict(model, dict())
    assert y == 0


def test_create_data_frame_missing_data(data):
    del data['small_bags']
    x = loader.create_avocado_data_frame(data)
    assert x is None


def test_prediction_missing_data(data):
    del data['small_bags']
    _ensure_model()
    y = predictor.predict(model, data)
    assert y == 0


def test_create_data_frame_invalid_date(data):
    data['date'] = 'invalid'
    x = loader.create_avocado_data_frame(data)
    assert x is None


def test_prediction_invalid_date(data):
    data['date'] = 'invalid'
    _ensure_model()
    y = predictor.predict(model, data)
    assert y == 0


def test_create_data_frame_invalid_type(data):
    data['organic'] = 'invalid'
    x = loader.create_avocado_data_frame(data)
    assert x is None


def test_prediction_invalid_type(data):
    data['organic'] = 'invalid'
    y = predictor.predict(model, data)
    assert y == 0


def test_create_data_frame_oov_region(data):
    data['region'] = 'oov'
    x = loader.create_avocado_data_frame(data)
    assert x is not None
    assert isinstance(x, pd.DataFrame)
    assert len(x.columns) == len(data)


def test_prediction_oov_region(data):
    data['region'] = 'oov'
    y = predictor.predict(model, data)
    assert y == 0
