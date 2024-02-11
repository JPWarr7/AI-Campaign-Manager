from app.forms.base import Form
from app.forms.fields import NumberField, FieldType


class SharesForm(Form):
	def __init__(self, name, title, values: dict = None):
		fields = {"quantity"}
		super().__init__(name, title=title, fields=fields, values=values or {})

	quantity = NumberField(
		field_type=FieldType.Number, label="Quantity", min_value=1,
		error_messages={"required": "Choose quantity!"}
	)


class AddSharesForm(SharesForm):
	def __init__(self):
		super().__init__(name="add-shares", title="Add Shares")


class RemoveSharesForm(SharesForm):
	def __init__(self):
		super().__init__(name="remove-shares", title="Remove Shares")
