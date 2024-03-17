from enum import StrEnum


class GitSourceType(StrEnum):
    TAG = 'tag'
    BRANCH = 'branch'
    COMMIT = 'commit'


class GithubSourceConfig:
    def __init__(self, repository_name: str, source_type: GitSourceType, source_name: str = None):
        self.repository_name = repository_name
        self.source_type = source_type
        self.source_name = source_name
