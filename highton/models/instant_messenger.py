from highton.models import HightonModel
from highton.highton_constants import HightonConstants
from highton import fields

class InstantMessenger(
    HightonModel,
):
    TAG_NAME = HightonConstants.INSTANT_MESSENGER

    def __init__(self, **kwargs):
        self.location = fields.StringField(name=HightonConstants.LOCATION)
        self.address = fields.StringField(name=HightonConstants.ADDRESS)
        self.protocol = fields.StringField(name=HightonConstants.PROTOCOL)

        super().__init__(**kwargs)
