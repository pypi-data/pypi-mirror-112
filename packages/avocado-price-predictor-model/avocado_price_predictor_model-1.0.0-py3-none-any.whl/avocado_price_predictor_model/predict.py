from sklearn import pipeline as sk_pipeline
from .load_data import create_avocado_data_frame


def predict(model: sk_pipeline.Pipeline, avocado: dict) -> float:
    """
    Parameters
    ----------
    model : sklearn.pipeline.Pipeline
        model to predict the price of a given avocado
    avocado : dict
        avocado instance data

    Returns
    -------
    float
        if avocado is valid, its predicted price is returned.
        otherwise , 0 is returned.

    Example
    -------
    import avocado_price_predictor_model.load_model as model_loader
    import avocado_price_predictor_model.predict as predictor

    avocado = {
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
    model = model_loader.load_model(https://ml-models.com/mymodel)
    if model:
        price = predictor.predict(model, avocado)
    """

    x = create_avocado_data_frame(avocado)
    y = 0.0
    if x is not None:
        try:
            y = model.predict(x).item()
        except:
            pass

    return round(y, 5)
