from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BasisModel(BaseModel):
    model_config = model_config
