from vc.client.schemas_base import ResponseData


class ClientException(Exception):
    def __init__(self, data, status_code, url):
        self.status_code = status_code
        self.data = data
        self.url = url

    def __str__(self):
        return f"{self.status_code}: {self.data} {self.url}"

    def to_dict(self):
        return dict(loc=["api"], msg=self.data, type=self.status_code)


def response_builder(expected_code=200, response_schema=ResponseData, data_schema=None):
    def wrapper(func):
        def builder(*args, **kwargs):
            data, status_code, url = func(*args, **kwargs)
            response = response_schema(status_code=status_code, url=url, **data)
            if status_code == expected_code:
                if data_schema:
                    try:
                        if isinstance(data, list):
                            response.data = data
                        else:
                            response.data = data_schema(**data)
                    except Exception as e:
                        print(data)
                        raise e
            else:
                raise ClientException(data, status_code, url)
            return response

        return builder

    return wrapper