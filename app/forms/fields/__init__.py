from enum import StrEnum


class FieldType(StrEnum):
    Text = "text"
    Password = "password"
    Number = "number"
    Switch = "switch"
    Telephone = "tel"
    Select = "select"
    Range = "range"


default_error_messages = {
    "required": "Please enter {0}!",
    "invalid": "Invalid value for {0}!"
}


class Field:
    def __init__(self, field_type: FieldType, label, value="", required=True, error_messages: dict[str, str] = None):
        self.type = field_type
        self.label = label
        self.required = required
        self.value = value
        self.error_messages = error_messages or {}

    def update(self, new_value: str):
        self.value = new_value

    def clear(self):
        self.value = ""

    def is_blank(self):
        return self.value == ""

    def validate(self, name: str):
        if self.required and self.is_blank():
            return False, self.fmt_error(name, "required")
        return True, ""

    def fmt_error(self, name: str, error_key: str):
        return self.error_messages[error_key].format(name)


class TextField(Field):
    def __init__(self, field_type=FieldType.Text, *args, **kwargs):
        super().__init__(field_type, *args, **kwargs)


class SelectOption:
    def __init__(self, display: str, value: str):
        self.display = display
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}: {self.display}"


class SelectField(Field):
    def __init__(self, options: list[SelectOption] = None, *args, **kwargs):
        self.options = options or []
        super().__init__(field_type=FieldType.Select, *args, **kwargs)


class NumberField(Field):
    def __init__(self, min_value=0, max_value=100, *args, **kwargs):
        self.min = min_value
        self.max = max_value
        field_type = kwargs.pop("field_type") or FieldType.Number
        super().__init__(field_type, *args, **kwargs)
