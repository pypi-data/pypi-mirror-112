import pickle
from base64 import b64decode, b64encode

from immutables import Map

from .models import Model


class Cursor:
    def __init__(
        self,
        direction: str = "asc",
        fields: list = (),
        obj: Model = None,
        or_fields: list = (),
        query_params: dict = Map(),
    ) -> None:
        self.direction = direction
        self.fields = fields
        self.obj = obj
        self.obj_fields = list((obj and obj.dict().keys()) or ())
        self.or_fields = or_fields
        self.query_params = query_params

    @classmethod
    def from_str(cls, model_cls, cursor: str = "", fields: list = ()) -> object:
        if cursor:
            direction, obj_dict, or_fields, query_params = pickle.loads(
                b64decode(cursor.encode("ascii"))
            )
            return cls(
                direction=direction,
                fields=fields,
                obj=model_cls(**obj_dict),
                or_fields=or_fields,
                query_params=query_params,
            )
        else:
            return cls(fields=fields)

    @property
    def obj_dict(self):
        return {k: getattr(self.obj, k) for k in self.obj_fields}

    def __eq__(self, other):
        return str(self) == str(other)

    def __repr__(self) -> str:
        return b64encode(
            pickle.dumps(
                (
                    self.direction,
                    self.obj_dict,
                    self.or_fields,
                    self.query_params or {},
                )
            )
        ).decode("ascii")
