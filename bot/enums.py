import enum


class CensorMode(enum.Enum):
    NORMAL = (
        "This will replace profanities in the message with a "
        "character set using `/options character`"
    )
    DELETE = "This will delete messages containing any profanities"
    SPOILER = (
        "This will wrap the profanities in a ||spoiler||. **NOTE:** This will "
        "also un-spoiler any text wrapped in spoiler tags!"
    )
