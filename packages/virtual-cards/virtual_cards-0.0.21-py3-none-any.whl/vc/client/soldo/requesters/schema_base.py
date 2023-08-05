from .utils import fingerprintHash, fingerprintSignature
from typing import Optional
from pydantic import Extra, BaseModel


class JWTData(BaseModel):
    refresh_token: str
    token_type: str
    access_token: str
    expires_in: int


class HeadersSoldoBase(BaseModel):
    """
    headers for Standard Authentication
    http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#standard-authentication
    """
    Authorization: Optional[str]

    def __init__(self, *args, **kwargs):
        from vc.manager import Soldo
        super().__init__(*args, **kwargs)
        self.Authorization = f"Bearer {Soldo.settings.ACCESS_TOKEN}"

    class Config:
        extra = Extra.allow


class HeadersSoldo(HeadersSoldoBase):
    """
    headers for Advanced Authentication
    http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#advanced-authentication
    """
    Content_Type: str = "application/json"
    fingerprintH: Optional[str]
    fingerprintS: Optional[str]

    def __init__(self, data, fields=None, **kwargs):
        from vc.manager import Soldo
        super().__init__(**kwargs)
        if not fields:
            fields = data.keys()
        fingerprint = ""
        for field in fields:
            f = data.get(field)
            if f is not None :
                if isinstance(f, bool):
                    f = str(f).lower()
                else:
                    f = str(f)
                fingerprint += f
                print(fingerprint)
        fingerprint += Soldo.settings.TOKEN
        print(fingerprint)
        self.fingerprintH = fingerprintHash(fingerprint)
        self.fingerprintS = fingerprintSignature(self.fingerprintH)

    class Config:
        fields = {
            "fingerprintS": "X-Soldo-Fingerprint-Signature",
            "fingerprintH": "X-Soldo-Fingerprint",
        }
        extra = Extra.allow
