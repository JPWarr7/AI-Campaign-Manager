from app.forms.base import Form
from app.forms.fields import SelectField, SelectOption, TextField


class ProfileForm(Form):
    def __init__(self, values: dict = None):
        fields = {"first_name", "last_name", "account_type"}
        super().__init__(name="profile", title="Create Profile",
                         fields=fields, values=values or {})

    first_name = TextField(
        label="First Name",
        error_messages={"required": "Enter first name!"})
    last_name = TextField(
        label="Last Name",
        error_messages={"required": "Enter last name!"})
    account_type = SelectField(
        label="I am",
        options=[
            SelectOption(display="A trader", value="Trader"),
            SelectOption(display="A broker", value="Broker"),
        ],
        error_messages={"required": "Choose account type"})
