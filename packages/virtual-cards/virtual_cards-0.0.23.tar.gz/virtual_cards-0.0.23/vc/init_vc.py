
def init_virtual_card(name:str, service: str,
                      uri: str,
                      celery_broker: str,
                      celery_backend: str,
                      user_model,
                      **config):
    from vc.manager import Soldo
    required_config = []
    network = None
    if "soldo" == service:
        network = Soldo

    return network(name, uri=uri, celery_broker=celery_broker, user_model=user_model, celery_backend=celery_backend,
                   **config)