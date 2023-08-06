from sd_utils.models.field import Field
from sd_utils.models.model import Model


class User(Model):
    name = Field(str, True)
    email = Field(str)
