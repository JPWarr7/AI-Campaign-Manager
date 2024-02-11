from collections import defaultdict
from .fields import Field, FieldType

clear_before_render = {FieldType.Password}


class Form:
    def __init__(self, name: str, title: str, fields: set, values: dict[str, str]):
        self.form_name = name
        self.title = title
        self.fields = fields
        self.errors: dict[str, str] = defaultdict(str)
        self.update(values)

    def get_field(self, name) -> Field:
        return getattr(self, name)

    def update(self, values: dict = None):
        for name, value in values.items() or {}:
            field = self.get_field(name)
            field.update(value)

    def clear(self):
        for name in self.fields:
            self.get_field(name).clear()

    def is_valid(self):
        form_valid = True
        for name in self.fields:
            field = self.get_field(name)
            (valid, message) = field.validate(name)
            self.errors[name] = message.format(name)
            if form_valid:
                form_valid = valid
        return form_valid

    def before_render(self):
        for name in self.fields:
            field = self.get_field(name)
            if field.type not in clear_before_render:
                continue
            field.clear()

    def values(self):
        values = {}
        for name in self.fields:
            field = self.get_field(name)
            values[name] = field.value
        return values.values()

    def __getitem__(self, name: str):
        return self.get_field(name).value

    def __str__(self):
        form_str = [self.title]
        for name in self.fields:
            field = self.get_field(name)
            form_str.append(f"{name}:\t{field.value}")
        return "\n".join(form_str)
