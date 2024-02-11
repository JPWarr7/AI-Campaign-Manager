from . import Form
from .fields import TextField, FieldType


class LoginForm(Form):
    def __init__(self, values: dict = None):
        fields = {"username", "password"}
        super().__init__(name="login", title="Log In",
                         fields=fields, values=values or {})

    username = TextField(
        label="Username",
        error_messages={"required": "Enter your username!"})
    password = TextField(
        label="Password",
        field_type=FieldType.Password,
        error_messages={"required": "Enter your password!"})
