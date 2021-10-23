import enum


class CensorMode(enum.Enum):
    normal = "Hide profanities from message."
    delete = "Delete messages containing profanities."
    spoiler = (
        "Wraps the profanities in a spoiler. NOTE: This will un-spoiler any "
        "text wrapped in spoiler tags."
    )
