import typing as T
import inspect
from pydantic import create_model, BaseModel


def computed_fields(fields: T.List[str]):
    FIELDS = fields

    def _computed_fields(cls: T.Type[BaseModel]) -> T.Type[BaseModel]:
        class NewClass(cls):
            def __init__(self, **data):
                base = cls(**data)
                for field in FIELDS:
                    if field not in data:
                        # if given, use the one given
                        data[field] = getattr(base, field)()
                super().__init__(**data)

            def dict(self, *args, **kwargs) -> T.Dict:
                for field in FIELDS:
                    setattr(self, f"{field}_", getattr(self, field)())
                d = super().dict(*args, **kwargs)
                return d

            class Config(cls.Config):
                fields = {f"{field}_": field for field in FIELDS}

        fields_d = {
            f"{field}_": (inspect.signature(getattr(cls, field)).return_annotation, ...)
            for field in FIELDS
        }
        final_class = create_model(cls.__name__, **fields_d, __base__=NewClass)
        return final_class

    return _computed_fields
