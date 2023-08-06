class Module:
    name: str = None
    version: str = None
    description: str = None

    def __init__(self, name: str, version: str, description: str = None):
        self.name = name
        self.description = description
        self.version = version
