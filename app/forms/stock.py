from app.forms.base import Form
from app.forms.fields import TextField


class StockForm(Form):
    def __init__(self, title="Add Stock", values: dict = None):
        fields = {"name", "code"}
        super().__init__(name="stock", title=title, fields=fields, values=values or {})

    name = TextField(
        label="Name",
        error_messages={"required": "Enter stock name!"})
    code = TextField(
        label="Code",
        error_messages={"required": "Enter stock code!"})


class DelistStockForm(Form):
    def __init__(self, title="Delist Stock", values: dict = None):
        super().__init__(name="stock", title=title, fields=set(), values=values or {})
