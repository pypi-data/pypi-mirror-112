import logging
import requests

from vc.libs.decoratos import response_builder
from .schema_base import HeadersSoldoBase, HeadersSoldo, JWTData
from vc.libs.utils import set_config


logger = logging.getLogger(__name__)
set_config(logger)


class RequesterSoldoBase(object):
    default_authorize = HeadersSoldoBase
    advanced_authorize = HeadersSoldo
    auth2_data: JWTData

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @response_builder(data_schema=JWTData)
    def oauth_authorize(self):
        from vc.manager import Soldo
        api_path = f'/oauth/authorize'
        response_data = self.request(
            api_path, method='post',
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"client_id": Soldo.settings.CLIENT_ID, "client_secret": Soldo.settings.CLIENT_SECRET})
        return response_data

    def request(
            self, path: str, method: str = "get", *,
            headers: dict = None,
            params: str = None, data: dict = None,
            json: dict = None,
            **kwargs):
        from vc.manager import Soldo
        r = requests.request(url=Soldo.settings.API_URL + path, method=method, headers=headers, json=json, data=data, params=params, **kwargs)
        logger.debug(f"request: {r.request.url}, b: {str(r.request.body)} h: {str(r.request.headers)}")
        logger.debug(f"response: {r.text}, b:  h: {r.headers}")
        if r.status_code == 401 and "invalid_token" in r.text:
            response_data = self.oauth_authorize()
            Soldo.settings.ACCESS_TOKEN = response_data.data.access_token
            headers["Authorization"] = Soldo.settings.ACCESS_TOKEN
            return self.request(path, method,  headers=headers,
                                params=params, data=data, json=json)

        data = r.text
        try:
            data = r.json()
        except:
            pass
        finally:
            # fix long response
            if isinstance(data, str):
                data = data[:400]
        return data, r.status_code, r.url
