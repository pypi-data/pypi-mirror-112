import attr
import typing


@attr.s(frozen=True)
class SensorField:
    tag: int = attr.ib()
    length: int = attr.ib()
    value: bytes = attr.ib()

    @classmethod
    def from_bytes(cls, data):
        if len(data) < 2:
            return None
        tag = data[0]
        length = data[1]
        if length > len(data):
            return None
        return cls(tag, length, data[2:2+length])

    def size(self):
        return self.length + 2


@attr.s(frozen=True)
class SensorReport:
    fields: typing.List[SensorField] = attr.ib(default=[])

    @classmethod
    def parse(cls, data):
        fields = []
        if len(data) < 2:
            sensor = cls()
            return sensor
        while data:
            field = SensorField.from_bytes(data)
            if not field:
                break
            fields.append(field)
            data = data[field.size():]
        return cls(fields)
