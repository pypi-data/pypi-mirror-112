from vc.libs.decoratos import response_builder
from .requesters.requester_base import RequesterSoldoBase
from .requesters.schemas import ResponseInfo, UserBase, Order, OrderItem, CardResponse, UserResponse, PaginateList, \
    WalletBase, ListRules, CardRule
import copy
from decimal import Decimal
from .requesters.utils import request_timestamp


class User(RequesterSoldoBase):

    @response_builder(data_schema=ResponseInfo)
    def whoami(self):
        api_path = f'/business/v2/ping/whoami'
        return self.request(api_path, method='get', headers=self.default_authorize().dict())

    @response_builder(data_schema=Order[OrderItem])
    def create(self, email: str, name: str, surname: str, custom_reference_id: str, job_title: str, **data):
        # http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#add-user
        api_path = f"/business/v2/employees/"

        user = UserBase(
            request_timestamp=request_timestamp(),
            surname=surname,
            name=name,
            email=email,
            custom_reference_id=custom_reference_id,
            job_title=job_title,
            mobile_access=False,
            web_access=False,
            **data).dict(exclude_none=True)
        h = self.advanced_authorize(
            user, fields=("request_timestamp", "name", "surname", "mobile_access", "web_access"),
        ).dict(by_alias=True)
        return self.request(
            api_path, method='post',
            headers=h,
            json=user)

    @response_builder(data_schema=UserBase)
    def update(self, id, **data):
        # http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#update-user-data
        api_path = f"/business/v2/employees/{id}"
        return self.request(
            api_path, method='put',
            headers=self.advanced_authorize(
                data, fields=("custom_reference_id", "job_title", "mobile_number", "mobile_prefix",
                              "email", "enable_mobile_credential", "enable_web_credential"),
            ).dict(by_alias=True),
            json=data)


class Wallets(RequesterSoldoBase):

    @response_builder(data_schema=ResponseInfo)
    def internal_transfer(self, amount: Decimal, toWalletId: str, fromWalletId: str, currencyCode: str= "EUR"):
        return self.request(
            f"/business/v2/wallets/internalTransfer/{fromWalletId}/{toWalletId}",
            method='put',
            headers=self.advanced_authorize(
                dict(toWalletId=toWalletId, fromWalletId=fromWalletId, amount=amount, currencyCode=currencyCode),
                fields=("amount", "currencyCode", "fromWalletId", "toWalletId")
            ).dict(by_alias=True), json=dict(amount=amount, currencyCode=currencyCode))

    @response_builder(data_schema=WalletBase)
    def get(self, wallet_id: str):
        return self.request(
            f"/business/v2/wallets/{wallet_id}",
            method='get',
            headers=self.default_authorize().dict())

    @response_builder(data_schema=PaginateList[WalletBase])
    def search(self, page=0, page_size=50, **data):
        data.update(dict(
            s=page_size,
            p=page,
        ))
        return self.request(
            "/business/v2/wallets",
            params=data,
            headers=self.default_authorize().dict()
        )

    @response_builder(data_schema=Order[OrderItem])
    def create(self, owner_type, currency, name, **kwargs):
        # http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#update-user-data
        # {
        # "id":"6a5e0887-eaf6-4f49-95cb-6b7f245d04f3",
        # "status":"PLACED","creation_time":"2021-06-29T10:42:06",
        # "last_update_time":"2021-06-29T10:42:06","is_valid":true,"total_paid_amount":0.000000,
        # "total_paid_currency":"EUR",
        # "items":[{"id":"87d95150-41f3-46a5-9501-ca1b368696ca","itemType":"WALLET","category":"WALLET"}]}
        api_path = f"/business/v2/wallets/"
        data = dict(request_timestamp=request_timestamp(), owner_type=owner_type, currency=currency, name=name,
                    **kwargs)
        h = self.advanced_authorize(
            data, fields=("request_timestamp", "owner_type", "currency", "name"),
        ).dict(by_alias=True)
        return self.request(
            api_path, method='post',
            headers=h, json=data)


class Card(RequesterSoldoBase):

    @response_builder(data_schema=Order[OrderItem])
    def create(self, wallet_id, owner_public_id: str = None, owner_type="company",
               type="VIRTUAL", name=None,
               emboss_line4=None, card_label="aff"):
        # http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#update-user-data
        api_path = f"/business/v2/cards/"
        data = dict(request_timestamp=request_timestamp(), name=name, emboss_line4=emboss_line4, owner_type=owner_type,
                    owner_public_id=owner_public_id,
                    wallet_id=wallet_id, type=type, card_label=card_label)
        h = self.advanced_authorize(
            data
            , fields=("request_timestamp", "owner_type", "owner_public_id", "wallet_id"),
        ).dict(by_alias=True)
        return self.request(
            api_path, method='post',
            headers=h, json=data)

    @response_builder(data_schema=CardResponse)
    def get(self, card_id: str, showSensitiveData: str = None):
        return self.request(
            f"/business/v2/cards/{card_id}", method='get',
            params={"showSensitiveData": showSensitiveData},
            headers=self.default_authorize().dict())

    @response_builder(data_schema=ListRules)
    def get_card_rules(self, card_id: str):
        return self.request(
            f"/business/v2/cards/{card_id}/rules", method='get',
            headers=self.default_authorize().dict())

    @response_builder(data_schema=ListRules)
    def update_card_rule(self, card_id: str, name, enabled=None, amount=None):
        data = CardRule(
            name=name,
            enabled=enabled,
            amount=amount).dict(exclude_none=None)
        print(data)
        data_h = copy.copy(data)
        # data_h["name"] = name.lower()
        return self.request(
            f"/business/v2/cards/{card_id}/rules", method='put', json=data,
            headers=self.advanced_authorize(
                data_h, fields=("name", "amount", "enabled")).dict(by_alias=True))

    @response_builder(data_schema=PaginateList[CardResponse])
    def search(self, page=0, page_size=50, **data):
        data.update(dict(
            s=page_size,
            p=page,
        ))
        return self.request(
            "/business/v2/cards",
            params=data,
            headers=self.default_authorize().dict()
        )


class Order(RequesterSoldoBase):

    @response_builder(data_schema=Order)
    def get(self, order_id: str):
        api_path = f"/business/v2/orders/{order_id}"
        return self.request(
            api_path, method='get',
            headers=self.default_authorize().dict())


class Group(RequesterSoldoBase):

    # @response_builder(data_schema=UserBase)
    def group_write(self, groupId: str, id: str, type: str):
        # http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#update-user-data
        data = dict(id=id, type=type)
        return self.request(
            f"/business/v2/groups/{groupId}/resource", method='post',
            headers=self.advanced_authorize(data).dict(by_alias=True), json=data)


class Transaction(RequesterSoldoBase):

    @response_builder(data_schema=PaginateList[ResponseInfo])
    def search(self, page=0, page_size=50, **params):
        params.update(dict(
            s=page_size,
            p=page,
        ))
        # http://apidoc-demo.soldo.com/v2/zgxiaxtcyapyoijojoef.html#update-user-data
        return self.request(
            f"/business/v2/transactions", method='get',
            params=params,
            headers=self.advanced_authorize(
                params,
                fields=(
                "type", "publicId", "customReferenceId", "groupId", "fromDate", "toDate", "dateType", "category",
                "status", "tagId", "metadataId", "text")
            ).dict(by_alias=True))


group = Group()
user = User()
wallets = Wallets()
card = Card()
order = Order()
transaction = Transaction()
