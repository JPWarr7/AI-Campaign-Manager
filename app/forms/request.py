from app.database.stocks import stock_broker_query
from app.database.shares import unowned_share_count, num_shares_owned
from app.database.requests import request_max
from app.forms.base import Form
from app.forms.fields import SelectField, SelectOption, NumberField, FieldType


class CreateRequestForm(Form):
    def __init__(self, brokers, name, title, max_value=100, values: dict = None):
        fields = {"amount", "bkr_id"}
        options = []
        for broker in brokers:
            name = f"{broker['first_name']} {broker['last_name']}"
            options.append(SelectOption(display=name, value=broker["usr_id"]))
        self.bkr_id.options = options
        self.amount.max = max_value
        super().__init__(name, title, fields=fields, values=values or {})

    amount = NumberField(field_type=FieldType.Range, label="Quantity", min_value=1,
                         error_messages={"required": "Choose quantity!"})
    bkr_id = SelectField(label="Broker", error_messages={"required": "Choose broker!"})


class CreateBuyRequestForm(CreateRequestForm):
    def __init__(self, stk_id, stk_name="", values: dict = None):
        valid, share_count = unowned_share_count(stk_id)
        if not valid:
            share_count = {}
        _, brokers = stock_broker_query(stk_id)
        super().__init__(brokers=brokers, name="buy", title=f"Buy {stk_name} Stock",
                         max_value=share_count.get("unowned", 0), values=values)
        # print(valid, share_count)
        # print(self.amount.max)


class CreateSellRequestForm(CreateRequestForm):
    def __init__(self, tdr_id, stk_id, stk_name="", values: dict = None):
        valid, share_count = num_shares_owned(stk_id, tdr_id=tdr_id)
        if not valid:
            share_count = {}
        _, brokers = stock_broker_query(stk_id, tdr_id)
        super().__init__(brokers, name="sell", title=f"Sell {stk_name} Stock",
                         max_value=share_count.get("owned", 0), values=values)
        # print(share_count)
        # print(self.amount.max)


class HandleRequestForm(Form):
    def __init__(self, req_id, stk_id, values: dict = None):
        fields = {"amount"}
        _, max_value = request_max(req_id)
        print(max_value)
        if not max_value:
            max_value = {}
        self.amount.max = max_value.get("value", 0)
        super().__init__(name="sell", title=f"Approve Request", fields=fields, values=values or {})

    amount = NumberField(field_type=FieldType.Range, label="Quantity", min_value=0,
                         error_messages={"required": "Choose quantity!"})
