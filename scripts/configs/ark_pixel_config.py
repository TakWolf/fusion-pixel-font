from enum import StrEnum


class SourceType(StrEnum):
    TAG = 'tag'
    BRANCH = 'branch'
    COMMIT = 'commit'


repository_name = 'TakWolf/ark-pixel-font'
source_type = SourceType.TAG
source_name = None
