from datetime import datetime

from sqlalchemy.orm import Session

from vc.models.soldo import WalletSo, CardSo


class EventMixer:
    format_date = "%Y-%m-%dT%H:%M:%SZ"

    # events functions

    def new_user(self, db: Session, **data):
        user = db.query(self._user).filter(self._user.email == data.get("email")).first()
        user.soldo_id = data.get("id")
        self.save_obj(db, user)

        if not data.get("groups"):
            self.add_item_to_group(user.soldo_id, type="USER")

        response_data = self.get_wallets(page_size=100)
        wallets = response_data.data.results
        wallets = list(filter(
            lambda w: w.primary_user_public_id == user.soldo_id,
            wallets))

        list_wallet_id = [w.search_id for w in user.wallet_soldo]

        wallets = list(filter(
            lambda w: w.id not in list_wallet_id,
            wallets
        ))

        for w in wallets:
            if w.currency_code in self.settings.currency:
                wallet = WalletSo(
                    user_id=user.id,
                    search_id=w.id,
                    balance=w.available_amount,
                    blocked_balance=w.blocked_amount,
                    currency=w.currency_code)
                if data.get("creation_time"):
                    wallet.created_on = datetime.strptime(data.get("creation_time"), self.format_date)
                self.save_obj(db, wallet)
        return user

    def wallet_created(self, db: Session, **data):
        """2021-07-02 12:56:37,564 - app.api.api_v1.endpoints.utils - DEBUG - b'{"event_type":"Wallet","event_name":"wallet_created",
        "data":
        {"id":"f0dd3007-838b-46e9-899c-3c526c71ee06","name":"test@test.com","currency_code":"USD","available_amount":0.00,"blocked_amount":0.00,"primary_user_type":"company","visible":true,"creation_time":"2021-07-02T09:56:37Z"}}'"""
        wallet = db.query(WalletSo).filter(WalletSo.search_id == data.get("id")).first()

        wallet.balance=data.get("available_amount"),
        wallet.blocked_balance=data.get("blocked_amount"),
        wallet.currency=data.get("currency_code")

        if data.get("creation_time"):
            wallet.created_on = datetime.strptime(data.get("creation_time"), self.format_date)
        self.save_obj(db, wallet)

        if not data.get("groups"):
            self.add_item_to_group(wallet.search_id)
        return wallet

    def store_order_completed(self, db, **data):
        print(data)
        order = self.get_cache_by_key(data.get("id"))
        print(order)
        for i in data.get("items"):
            category = i.get("category")
            print(category)
            if category == "CARD":
                print(i)
                print(order)
                card = db.query(CardSo).filter(CardSo.search_id==i.get("id")).first()
                if not card:
                    card = CardSo(search_id=i.get("id"), wallet_id=order.get("wallet_id"))
                    self.save_obj(db, card)

                card = self.update_info_card(db, card.id)
                print(card)
                print(card.__dict__)
                self.add_item_to_group(card.search_id, type="CARD")
                self.wallet_update_balance(db, card.wallet_id)
                self.remove_cache(data.get("id"))