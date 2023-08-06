from typing import Optional
from os import remove
from pickle import loads
from gdown import download
from sklearn import pipeline as sk_pipeline


def load_model(url: str) -> Optional[sk_pipeline.Pipeline]:
    """
    Parameters
    ----------
    url : str
        url to download the model from.

    Returns
    -------
    Optional[sklearn.pipeline.Pipeline] - sklearn.pipeline.Pipeline or None
        if model is downloaded successfully and loaded as sklearn.pipeline.Pipeline, it's returned.
        otherwise, returns None.

    Example
    -------
    import avocado_price_predictor_model.load_model as model_loader

    model = model_loader.load_model(https://ml-models.com/mymodel)
    """
    # download model
    tmp_file = download(url, 'tmp.pkl')

    # load model from file to memory
    with open(tmp_file, 'rb') as f:
            raw = f.read()

    # delete file
    remove(tmp_file)

    try:
        model = loads(raw)
    except:
        return None

    if isinstance(model, sk_pipeline.Pipeline):
        return model
    
    return None
