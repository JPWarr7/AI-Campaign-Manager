from . import Form
from .fields import TextField, FieldType


class RegisterForm(Form):
    def __init__(self, values: dict = None):
        fields = {"username", "password", "confirm"}
        super().__init__(name="register", title="Register",
                         fields=fields, values=values or {})

    username = TextField(label="Username",
                         error_messages={"required": "Enter a username!"})
    password = TextField(label="Password", field_type=FieldType.Password,
                         error_messages={"required": "Enter a password!"})
    confirm = TextField(label="Confirm Password", field_type=FieldType.Password,
                        error_messages={"required": "Re-enter your password!"})
